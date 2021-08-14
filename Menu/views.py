from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators import http

from Menu.forms import MenuForm
from Menu.models import Menu, Item
from Ordering.models import Order
from Yummy.models import Restaurant
from utility.opening_utility import today_opening_time
from utility.restaurant_utility import makePaginate


def FilterByData(request_GET):
    type_array = request_GET.getlist('type[]')
    rating = request_GET['rating']
    isTakeAway = True if request_GET['isTakeAway'] == "true" else False
    isDelivery = True if request_GET['isDelivery'] == "true" else False
    popularity = request_GET['popularity']
    restaurant = Restaurant.objects.filter(
        tags__name__in=type_array,
        rating__gt=rating,
        is_take_away=isTakeAway,
        is_delivery=isDelivery,
        is_popular=False if popularity == 'false' else True
    ).distinct()
    return restaurant


@http.require_GET
def Menu_of_restaurant(request, id):
    """ GET menu of restaurant by id """
    restaurant = get_object_or_404(Restaurant, id=id)
    order_list = Order.objects.get(user=request.user, is_paid=False)
    items = Item.objects.filter(restaurant_id=id)

    starter = items.filter(category='Starter')
    main_course = items.filter(category='Main course')
    beef = items.filter(category='Beef')
    dessert = items.filter(category='Dessert')
    drink = items.filter(category='Drink')
    context = {
        'restaurant': restaurant,
        'order_list': order_list,
        'starter': starter,
        'main_course': main_course,
        'beef': beef,
        'dessert': dessert,
        'drink': drink,
    }
    return render(request, 'restaurant/menu.html', context)


@http.require_GET
def filter_restaurants(request, page):
    """
    GET:
        Get restaurants by filters params that send via AJAX
        Paginate filtered restaurants
        Send context to the page that the user is coming from it
    """
    if request.is_ajax():
        allRestaurant = FilterByData(request.GET)
        context = {
            'allRestaurant': makePaginate(allRestaurant, page),
            'today_weekday': today_opening_time(allRestaurant),
        }

        senderPath = request.GET['senderPath']
        if '/list_page/' in senderPath:
            template = 'include/grid_list/list.html'
        elif '/grid_list/' in senderPath:
            template = 'include/grid_list/grid.html'
        else:
            return JsonResponse({}, status=400)
        return render(request, template, context)


@login_required
@http.require_GET
def admin_section(request):
    """ This is a page that owners can moderate their menus """
    if not request.user.isOwner:
        raise HttpResponseForbidden

    restaurant = get_object_or_404(Restaurant, owner=request.user)
    items = Item.objects.filter(
        menu__restaurant=restaurant).order_by('name')
    form = MenuForm()
    context = {
        'restaurant': restaurant,
        'items': items,
        'form': form,
    }
    return render(request, 'main_pages/admin_section.html', context)


@login_required
@http.require_POST
def deleteItem_form(request):
    """ Delete item from menu via AJAX """
    if not request.user.isOwner:
        raise HttpResponseForbidden

    if request.is_ajax():
        item_ID = request.POST['item_ID']
        item = Item.objects.filter(id=item_ID).order_by('name')
        try:
            item.delete()
            response = JsonResponse({'result': 'success'})
        except:
            response = JsonResponse({'result': 'error'}, status=400)
        return response


@login_required
@http.require_POST
def addItem_form(request):
    """ Add new item to menu via AJAX """
    if not request.user.isOwner:
        raise HttpResponseForbidden

    if request.is_ajax():
        form = MenuForm(request.POST or None, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.menu = Menu.objects.get(restaurant__owner=request.user)
            item.save()
            menu = Item.objects.filter(menu__restaurant__owner=request.user)
            return render(request,
                          'include/../templates/restaurant/menu_items.html', {'menu': menu})


@login_required
@http.require_POST
def updateItem_form(request):
    """ Update data of item via AJAX """
    if not request.user.isOwner:
        raise HttpResponseForbidden

    if request.is_ajax():
        edited_item = request.POST
        item = Item.objects.get(id=edited_item['id'])
        item.name = edited_item['name']
        item.category = edited_item['category']
        item.price = edited_item['price']
        item.description = edited_item['description']
        item.save()
        return JsonResponse({})
