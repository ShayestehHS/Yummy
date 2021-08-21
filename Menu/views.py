import json

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


def FilterByData(received_data):
    type_array = received_data['type']
    rating = received_data['rating']
    is_take_away = True if received_data['isTakeAway'] == "true" else False
    is_delivery = True if received_data['isDelivery'] == "true" else False
    is_popular = True if received_data['popularity'] == "true" else False
    restaurant = Restaurant.objects.filter(
        tags__name__in=type_array,
        rating__gt=rating,
        is_take_away=is_take_away,
        is_delivery=is_delivery,
        is_popular=is_popular,
    ).order_by('name').distinct()
    return restaurant


@http.require_GET
def Menu_of_restaurant(request, id):
    """ GET menu of restaurant by id """
    restaurant = get_object_or_404(Restaurant, id=id)
    order_list = Order.objects.get(user=request.user, is_paid=False)
    items = Item.objects.filter(menu__restaurant=restaurant)

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


@http.require_POST
def filter_restaurants(request, page):
    """
    POST:
        Getting restaurants by filters params that send via AJAX
        Paginate filtered restaurants
        Send context to the page that the user is coming from it
    """
    if request.is_ajax():
        received_json_data = json.loads(request.body)
        filtered_restaurants = FilterByData(received_json_data)
        context = {
            'allRestaurant': makePaginate(filtered_restaurants, page),
            'today_weekday': today_opening_time(filtered_restaurants),
        }

        sender_path = received_json_data['senderPath']
        if '/list_page/' in sender_path:
            template = 'include/grid_list/list.html'
        elif '/grid_list/' in sender_path:
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
        received_json_data = json.loads(request.body)
        item_id = received_json_data['item_ID']
        item = Item.objects.filter(id=item_id).order_by('name')
        try:
            item.delete()
            response = JsonResponse({'result': 'success'}, status=200)
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
        form = MenuForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            menu = Menu.objects.get(restaurant__owner=request.user)
            item = form.save(commit=False)
            item.menu = menu
            item.save()
            items = Item.objects.filter(menu=menu)
            return render(request,
                          'restaurant/menu_items.html', {'items': items})



@login_required
@http.require_POST
def updateItem_form(request):
    """ Update data of item via AJAX """
    if not request.user.isOwner:
        raise HttpResponseForbidden

    if request.is_ajax():
        edited_item = json.loads(request.body)
        item = Item.objects.get(id=edited_item['id'])

        item.name = edited_item['name']
        item.category = edited_item['category']
        item.price = edited_item['price']
        item.description = edited_item['description']

        item.save()
        return JsonResponse({}, status=200)
