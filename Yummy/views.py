from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators import http
from django.views.generic import TemplateView
from taggit.models import Tag
from termcolor import colored

import Ordering.models as ordering_models
import Yummy.forms as yummy_forms
import Yummy.models as yummy_models
from Yummy_site.settings import MAPBOX_KEY
from utility import restaurant_utility, opening_utility
from utility.EmailService import EmailService


def baseContext(allRestaurant):
    """ Generate contexts for Basics elements of main_pages """
    tags = Tag.objects.annotate(
        num_tag=Count('taggit_taggeditem_items')).order_by('-num_tag')
    context = {
        'allRestaurant_Count': yummy_models.Restaurant.objects.all().count(),
        'allRestaurant': allRestaurant,
        'today_weekday': opening_utility.today_opening_time(allRestaurant),
        'tags': tags,
    }
    return context


def get_listing_page_context(request, page):
    """ Generate context of List and Grid functions """
    searched_key = request.GET.get('key')
    allRestaurant = restaurant_utility.get_allRestaurant(searched_key, page)

    context = {'searched_key': searched_key, }
    context.update(baseContext(allRestaurant))

    return context


@http.require_GET
def Home(request):
    PopularRestaurant = yummy_models.Restaurant.objects.filter(
        is_popular=True)[:6]
    restaurant_count = yummy_models.Restaurant.objects.count()
    user_count = get_user_model().objects.count()
    served_count = ordering_models.Order.objects.filter(
        is_paid=True).count()
    context = {
        'PopularRestaurant': PopularRestaurant,
        'restaurant_count': restaurant_count,
        'user_count': user_count,
        'served_count': served_count,
        'today_weekday': opening_utility.today_opening_time(
            PopularRestaurant),
    }
    welcomeMSG = request.user.get_full_name() if request.user.is_authenticated else ""
    messages.success(request, "Welcome " + welcomeMSG)
    return render(request, 'main_pages/home.html', context)


@http.require_GET
def List(request, page=1):
    """
    List all restaurants in a paginated list
    or
    Show result of restaurant by searched key
    """
    context = get_listing_page_context(request, page)
    return render(request, 'restaurant/list_page.html', context)


@http.require_GET
def Grid(request, page=1):
    """
    Show all restaurants in a paginated grid list
    or
    Show result of restaurant by searched key
    """
    context = get_listing_page_context(request, page)
    return render(request, 'restaurant/grid_list.html', context=context)


@login_required
def Submit_driver(request):
    """
    Default: Check requested user is driver or not
    GET: Show form to user
    POST:
        Check validation of form
        Update requested user as driver
        Send email to requested user and superUsers
    """
    if request.user.isDriver:
        messages.error(request, 'You are submitted before')
        return redirect('home')

    if request.method == 'POST':
        # Saving data of driver
        form = yummy_forms.DriverForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user
            driver.save()
            request.user.isDriver = True

            # Getting emails of: admins
            admin_emails = get_user_model().objects.filter(
                is_superuser=True).values_list('email', flat=True)

            # Send email to [admin_email]
            context = {
                'title': 'New request for driver',
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'username_id': request.user.id,
            }
            EmailService.send_email(
                title='New request for driver',
                to=admin_emails,
                context=context,
                template_name='email/DriverEmail.html')
            messages.success(request,
                             "Your request is sent\n"
                             "Wait for request from restaurants")
            return redirect('home')
        else:
            # else => form is not valid
            messages.error(request,
                           'We have a problem with your form\n'
                           'Please try again')
            return render(request,
                          'restaurant/../templates/ submission/submit_driver.html')
    elif request.method == 'GET':
        if not request.user.isDriver:
            form = yummy_forms.DriverForm
            context = {'form': form}
            return render(request,
                          'restaurant/../templates/ submission/submit_driver.html', context)

        # User is: submitted driver
        messages.error(request, 'You are submitted before')
        return redirect('home')


@login_required
def Submit_restaurant(request):
    """
    Default: Check requested user is driver or not
    GET: Show form to user
    POST:
        Check validation of form
        Update requested user as owner
        Send email to requested user and superUsers
    """
    if request.user.isOwner:
        messages.error(request, 'You are submitted before')
        return redirect('home')

    if request.method == 'GET':
        form = yummy_forms.SubmitRestaurantForm
        context = {'form': form, }
        return render(request,
                      'restaurant/../templates/ submission/submit_restaurant.html', context)

    elif request.method == 'POST':
        form = yummy_forms.SubmitRestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()

            request.user.update(IsOwner=True)

            # Getting emails of: admins
            admin_emails = get_user_model().objects.filter(
                is_superuser=True).values_list('email', flat=True)

            # Send email to [admin_email]
            context = {
                'title': 'New request for restaurant',
                'email': request.user.email,
                'username': request.user.username,
                'restaurant_name': form.cleaned_data['name'],
                'restaurant_city': form.cleaned_data['city'],
                'restaurant_website': form.cleaned_data['website_url'],
                'restaurant_id': restaurant.id,
            }
            EmailService.send_email(title='New request for restaurant',
                                    to=admin_emails, context=context,
                                    template_name='email/RestaurantEmail.html')

            messages.success(request,
                             'Your message is sent\n'
                             'Wait for response from your email')
        else:
            # else => form is not valid
            messages.error(request, 'Please try again')
        return redirect('home')


@http.require_GET
def Detail_restaurant(request, Re_id):
    """ GET restaurant by ID and show the detail of it """
    if request.method == 'GET':
        form = yummy_forms.NewReviewForm
        restaurant = yummy_models.Restaurant.objects.get(id=Re_id)
        restaurant_img = yummy_models.RestaurantImage.objects.filter(
            restaurant=restaurant).all()
        Opening_time = yummy_models.OpeningTime.objects.filter(
            restaurant=restaurant).values_list(
            'weekday', 'from_hour', 'to_hour').all()
        review = yummy_models.RestaurantReview.objects.filter(
            restaurant=restaurant).all()

        data = {
            'restaurant': restaurant,
            'image': restaurant_img,
            'today_weekday': opening_utility.get_opening_times(Opening_time),
            'mapbox_access_token': MAPBOX_KEY,
            'review': review,
            'form': form,
        }
        return render(request, 'restaurant/detail_restaurant.html', data)


@http.require_GET
def Search(request, page=1):
    """GET key from request and filter and paginate all restaurants by name """
    key = request.GET['key']
    filteredRestaurant = yummy_models.Restaurant.objects.filter(
        name__contains=key)
    paginatedRestaurant = restaurant_utility.makePaginate(
        objects=filteredRestaurant, page_number=page)

    context = {'searched_key': key, }
    context.update(baseContext(paginatedRestaurant))
    return render(request, 'restaurant/list_page.html', context=context)


def Save_review(request, Re_id):
    """ Save review of restaurant via AJAX """
    if request.is_ajax() and request.method == 'POST':
        restaurant = yummy_models.Restaurant.objects.get(id=Re_id)
        form = yummy_forms.NewReviewForm(request.POST)
        userReview = yummy_models.RestaurantReview.objects.filter(
            user=request.user,
            restaurant=restaurant)
        if not userReview.exists():
            if form.is_valid():
                data = {}
                review = form.save(commit=False)
                review.author = request.user
                review.restaurant = restaurant  # Restaurant.objects.get(id=id)
                review.save()
                # The success message is sent via ShowMessageAjax.
                data['success'] = 'Your review is saved'
                data['review'] = review.description
                return JsonResponse(data)
            else:
                # else => form is not valid
                print(colored(f'userReview is not valid ', 'red'))
                return JsonResponse({'error': 'Your form is not valid'})
        else:
            # else => User want to submit second review
            return JsonResponse({'error': "You can't submit a review again"})


@http.require_GET
def Search_tag(request, tag_slug, page=1):
    """
    GET tag_slug from url and search between all restaurants by tag name
    """
    filteredRestaurant = yummy_models.Restaurant.objects.filter(
        tags__slug__in=[tag_slug]).order_by('name')
    paginatedRestaurant = restaurant_utility.makePaginate(
        filteredRestaurant, page)

    context = {'searched_tag': tag_slug, }
    context.update(baseContext(paginatedRestaurant))

    if 'list_page' in request.path:
        return render(request, 'restaurant/list_page.html', context)
    elif 'grid_list' in request.path:
        return render(request, 'restaurant/grid_list.html', context)


@http.require_GET
def Sort_restaurants(request, page):
    """
    GET parameter from request:
        If key is exists in path => We searched restaurants by name
        If tag is exists in path => We searched restaurants by tag name
        Else => The request is coming from the basic 'list' and 'gridList' page

    At the end:
        Set the destination of request by
        the page that the request is coming from.
    """
    mode = request.GET.get('mode', 'name')
    mode = 'rating' if mode == 'lower' else '-rating' if mode == 'higher' else 'name'

    if request.GET.get('key') is not None:
        allRestaurant = yummy_models.Restaurant.objects.filter(
            name__contains=request.GET['key']).order_by(mode)
    elif request.GET.get('tag') is not None:
        allRestaurant = yummy_models.Restaurant.objects.filter(
            tags__slug__in=[request.GET['tag']]).order_by(mode)
    else:
        allRestaurant = yummy_models.Restaurant.objects.all().order_by(mode)
    context = {
        'allRestaurant': restaurant_utility.makePaginate(allRestaurant, page),
        'today_weekday': opening_utility.today_opening_time(allRestaurant),
    }

    senderPath = request.GET.get('senderPath')
    if '/list_page/' in senderPath:
        render(request, "include/grid_list/list.html", context)
    elif '/grid_list/' in senderPath:
        render(request, 'include/grid_list/grid.html', context)
    else:
        return JsonResponse({}, status=400)


class About_us(TemplateView):
    template_name = 'main_pages/about_us.html'


class Faq(TemplateView):
    template_name = 'main_pages/faq.html'


def Contacts(request):
    """
    GET: render contact page
    POST: Send email from user to admin
    """
    if request.method == "GET":
        return render(request, 'main_pages/contacts.html')

    elif request.is_ajax() and request.method == "POST":
        title = 'Email from user'
        superUser_email = get_user_model().objects.filter(
            is_superuser=True).values_list('email', flat=True)

        EmailService.send_email(
            title=title,  # Title of email
            to=superUser_email,
            context={
                'title': title,  # Title of Email text
                'name': request.POST.get('name', "'null'"),
                'family': request.POST.get('family', "'null'"),
                'email': request.POST.get('email', '#/'),
                'text': request.POST.get('text', 'An error occurred'),
            },
            template_name='email/UserEmail.html', )
        return JsonResponse({})
