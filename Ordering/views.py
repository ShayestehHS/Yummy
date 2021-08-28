from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators import http
from termcolor import colored

from Menu.models import Item
from Ordering.forms import Step1Form
from Ordering.models import CartItem, Order, OrderDetail
from utility import custom_decorators


@login_required
def Step_1(request):
    """
        GET: Rendering the step_1 page
        POST: Save the OrderDetail of Order object
    """
    order = Order.objects.get(user=request.user, is_paid=False)
    if request.method == "GET":
        if order.cartItems.count() == 0:
            messages.error(request, "Your order list is empty")
            return redirect('home')

        form = Step1Form()
        delivery_charge = Order.objects.get(user=request.user).restaurant.delivery_charge
        return render(request, 'ordering/step_1.html', {'order_list': order,
                                                        'delivery_charge': delivery_charge,
                                                        'form': form})

    elif request.method == 'POST':
        form = Step1Form(data=request.POST)

        if not form.is_valid():
            messages.error(request, 'Your data is invalid')
            return HttpResponseRedirect(reverse('step_1'))

        step1_data = form.save(commit=False)
        step1_data.order = order
        step1_data.save()

        return HttpResponseRedirect(reverse('step_2'))


@login_required
def Step_2(request):
    if request.method == "GET":
        order_detail = OrderDetail.objects.filter(order__user=request.user)
        if not order_detail.exists():
            messages.error(request, 'You have to complete step_one first')
            return HttpResponseRedirect(reverse('step_1'))

        order = Order.objects.get(user=request.user, is_paid=False)
        order_detail = order_detail.first()
        delivery_charge = Order.objects.get(user=request.user).restaurant.delivery_charge
        return render(request, 'ordering/step_2.html', {'order_list': order,
                                                        'delivery_charge': delivery_charge,
                                                        'order_detail': order_detail})
    elif request.method == "POST":
        payment_page = None  # Payment page is not applied yet
        if payment_page:
            return payment_page

        return HttpResponseRedirect(reverse('step_3'))


@http.require_GET
@login_required
def Step_3(request):
    old_order = Order.objects.get(user=request.user, is_paid=False)
    old_order.is_paid = True
    old_order.save(update_fields=['is_paid'])

    Order.objects.create(user=request.user, is_paid=False)

    context = {
        'order_list': old_order,
        'cartItems': old_order.cartItems.all(),
        'order_detail': OrderDetail.objects.get(order=old_order),
    }
    messages.success(request, "Your order is on the way")
    return render(request, 'ordering/step_3.html', context)


@http.require_POST
@custom_decorators.require_ajax
def UpdateCarts(request):
    """ Add or Remove Item from order_list by AJAX """
    item_id = request.POST["item_id"]
    item_mode = request.POST["item_mode"]
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)
    item = Item.objects.select_related('menu__restaurant').get(id=item_id)

    if created or order.restaurant is None:  # restaurant is None => First time of adding Item to order_list
        order.restaurant = item.menu.restaurant
        order.restaurant.save()
    elif order.restaurant != item.menu.restaurant:
        return JsonResponse({"errorMsg": f"This item does not belong to '{order.restaurant}'"})

    cart_item = CartItem.objects.get_or_create(order=order, item=item)[0]
    quantity = cart_item.Add() if item_mode == "plus" else cart_item.Remove() or 0
    data = {
        "quantity": quantity,
        "total_price": cart_item.total_price,
    }
    return JsonResponse(data)
