from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators import http
from django.views.generic import TemplateView
from taggit.models import Tag

import Ordering.models as ordering_models
from Yummy.forms import Review_Form, SubmitRestaurantForm, DriverForm
from Yummy.models import OpeningTime, Restaurant, RestaurantImage, RestaurantReview
from Yummy_site.settings import MAPBOX_KEY
from utility import restaurant_utility, opening_utility, custom_decorators
from utility.EmailService import EmailService


def base_context(all_restaurants):
    """ Generate contexts for Basics elements of main_pages """
    tags = Tag.objects.annotate(
        num_tag=Count('taggit_taggeditem_items')).order_by('-num_tag')
    context = {
        'allRestaurant_Count': Restaurant.objects.all().count(),
        'allRestaurant': all_restaurants,
        'today_weekday': opening_utility.today_opening_time(all_restaurants),
        'tags': tags,
    }
    return context


def get_listing_page_context(request, page):
    """ Generate context of List and Grid functions """
    searched_key = request.GET.get('key')
    all_restaurants = restaurant_utility.get_allRestaurant(searched_key, page)

    context = {'searched_key': searched_key, }
    context.update(base_context(all_restaurants))

    return context


@http.require_GET
def Home(request):
    popular_restaurant = Restaurant.objects.filter(is_popular=True)[:6]
    restaurant_count = Restaurant.objects.count()
    user_count = get_user_model().objects.count()
    served_count = ordering_models.Order.objects.filter(is_paid=True).count()

    context = {
        'PopularRestaurant': popular_restaurant,
        'restaurant_count': restaurant_count,
        'user_count': user_count,
        'served_count': served_count,
        'today_weekday': opening_utility.today_opening_time(popular_restaurant),
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

    if request.method == 'GET':
        form = DriverForm
        context = {'form': form}
        return render(request, 'submission/submit_driver.html', context)

    if request.method == 'POST':
        # Saving data of driver
        form = DriverForm(data=request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user
            driver.save()

            user = get_user_model().objects.get(email=request.user.email)
            user.isDriver = True
            user.save(update_fields=['isDriver'])

            # Getting emails of: admins
            admin_emails = get_user_model().objects.filter(
                is_superuser=True).values_list('email', flat=True)

            # Send email to [admin_email]
            context = {
                'title': 'New request for driver',
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username_id': user.id,
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
            return render(request, 'submission/submit_driver.html')


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
        form = SubmitRestaurantForm
        context = {'form': form, }
        return render(request, 'submission/submit_restaurant.html', context)

    if request.method == 'POST':
        form = SubmitRestaurantForm(data=request.POST, files=request.FILES)
        form.owner = request.user
        if form.is_valid():
            user = get_user_model().objects.get(email=request.user.email)

            user.isOwner = True
            user.save(update_fields=['isOwner'])

            restaurant = form.save(commit=False)
            restaurant.owner = user
            restaurant.save()

            # Getting emails of: admins
            admin_emails = get_user_model().objects.filter(
                is_superuser=True).values_list('email', flat=True)

            # Send email to [admin_email]
            context = {
                'title': 'New request for restaurant',
                'email': user.email,
                'username': user.username,
                'restaurant_name': form.cleaned_data['name'],
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
    form = Review_Form
    restaurant = Restaurant.objects.get(id=Re_id)
    restaurant_img = RestaurantImage.objects.filter(
        restaurant=restaurant).all()
    opening_time = OpeningTime.objects.filter(
        restaurant=restaurant).values_list(
        'weekday', 'from_hour', 'to_hour').all()
    review = RestaurantReview.objects.filter(
        restaurant=restaurant).all()

    data = {
        'restaurant': restaurant,
        'image': restaurant_img,
        'today_weekday': opening_utility.get_opening_times(opening_time),
        'mapbox_access_token': MAPBOX_KEY,
        'review': review,
        'form': form,
    }
    return render(request, 'restaurant/detail_restaurant.html', data)


@http.require_POST
@custom_decorators.required_ajax
@login_required
def Save_review(request, Re_id):
    """ Save review of restaurant via AJAX """
    restaurant = Restaurant.objects.get(id=Re_id)
    review_by_user = RestaurantReview.objects.filter(restaurant=restaurant, user=request.user)
    if review_by_user.exists():
        return JsonResponse({'error': "You can't submit a review again"})

    form = Review_Form(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.restaurant = restaurant  # Restaurant.objects.get(id=id)
        review.save()
        # The success message is sent via ShowMessageAjax.
        data = {
            'success': 'Your review is saved',
            'review': review.description
        }
        return JsonResponse(data)
    else:
        # else => form is not valid
        return JsonResponse({'error': 'Your form is not valid'})


@http.require_GET
def Search(request, page=1):
    """GET key from request and filter and paginate all restaurants by name """
    key = request.GET['key']
    filtered_restaurant = Restaurant.objects.filter(name__contains=key).order_by('name')
    paginated_restaurant = restaurant_utility.makePaginate(objects=filtered_restaurant,
                                                           page_number=page)

    context = {'searched_key': key, }
    context.update(base_context(paginated_restaurant))
    return render(request, 'restaurant/list_page.html', context=context)


@http.require_GET
def Search_tag(request, tag_slug, page=1):
    """ GET tag_slug from url and search between all restaurants by tag name """
    filtered_restaurants = Restaurant.objects.filter(
        tags__slug__in=[tag_slug]).order_by('name')
    paginated_restaurants = restaurant_utility.makePaginate(
        filtered_restaurants, page)

    context = {'searched_tag': tag_slug, }
    context.update(base_context(paginated_restaurants))

    if 'list_page' in request.path:
        return render(request, 'restaurant/list_page.html', context)
    elif 'grid_list' in request.path:
        return render(request, 'restaurant/grid_list.html', context)


@http.require_POST
@custom_decorators.required_ajax
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
    mode = request.POST.get('mode', default='name')
    mode = 'rating' if mode == 'lower' else '-rating' if mode == 'higher' else 'name'

    if request.POST.get('key') is not None:
        all_restaurants = Restaurant.objects.filter(
            name__contains=request.POST['key']).order_by(mode)
    elif request.POST.get('tag') is not None:
        all_restaurants = Restaurant.objects.filter(
            tags__slug__in=[request.POST['tag']]).order_by(mode)
    else:
        all_restaurants = Restaurant.objects.all().order_by(mode)

    context = {
        'allRestaurant': restaurant_utility.makePaginate(all_restaurants, page),
        'today_weekday': opening_utility.today_opening_time(all_restaurants),
    }

    sender_path = request.POST.get('senderPath')
    if '/list_page/' in sender_path:
        return render(request, "include/grid_list/list.html", context)
    elif '/grid_list/' in sender_path:
        return render(request, 'include/grid_list/grid.html', context)
    else:
        return JsonResponse({}, status=400)


def contact_to_us(request):
    """
    GET: render contact page
    POST: Send email from user to admin
    """
    if request.method == "GET":
        return render(request, 'main_pages/contacts.html')

    if request.method == "POST" and request.is_ajax():
        title = 'Email from user'
        super_user_emails = get_user_model().objects.filter(
            is_superuser=True).values_list('email', flat=True)

        EmailService.send_email(
            title=title,  # Title of email
            to=super_user_emails,
            context={
                'title': title,  # Title of Email text
                'name': request.POST.get('name', "'null'"),
                'family': request.POST.get('family', "'null'"),
                'email': request.POST.get('email', '#/'),
                'text': request.POST.get('text', 'An error occurred'),
            },
            template_name='email/UserEmail.html'
        )
        return JsonResponse({'success': "We received your emailThanks for your email", })


class AboutUs(TemplateView):
    template_name = 'main_pages/about_us.html'


class Faq(TemplateView):
    template_name = 'main_pages/faq.html'
