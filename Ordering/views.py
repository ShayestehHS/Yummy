from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from termcolor import colored

from Menu.models import Item
from Ordering.models import CartItem, Order, OrderDetail


@login_required
def Step_1(request):
    order = Order.objects.get(user=request.user, is_paid=False)
    if request.method == "GET":
        if order.cartItems.count() > 0:
            order_detail = OrderDetail.objects.filter(order=order).first()
            return render(request, 'ordering/step_1.html', {'order_list': order,
                                                             'order_detail': order_detail})
        else:
            # else => order_list is empty
            messages.error(request,"Your order list is empty")
            return redirect('home')

    elif request.method == 'POST':
        order_detail = OrderDetail.objects.get_or_create(order=order)[0]
        order_detail.telephone = request.POST['tel_order']
        order_detail.full_address = request.POST['address_order']
        order_detail.postal_code = request.POST['pcode_order']
        order_detail.deliveryDay = request.POST['delivery_schedule_day']
        order_detail.deliveryTime = request.POST['delivery_schedule_time']
        order_detail.description = request.POST.get('notes')
        order_detail.deliveryMethod = request.POST['method']
        order_detail.save()
        return HttpResponseRedirect(reverse('step_2'))


@login_required
def Step_2(request):
    if request.method == 'GET':
        order_detail = OrderDetail.objects.filter(order__user=request.user)
        if order_detail.exists():
            order_detail = order_detail.first()
            order = Order.objects.get(user=request.user, is_paid=False)
            return render(request, 'ordering/step_2.html', {'order_list': order,
                                                             'order_detail': order_detail})
        else:
            messages.error(request, 'You have to complete step_one first.')
            return HttpResponseRedirect(reverse('step_1'))


@login_required
def Step_3(request):
    if request.method == 'GET':
        try:
            order = Order.objects.get(user=request.user, is_paid=False)
        except Order.DoesNotExist:
            return redirect('home')
        except Order.MultipleObjectsReturned:
            print(colored(f'We have an error in ( Ordering => views => Step_3 )', 'red'))
            Order.objects.filter(user=request.user).delete()
            Order.objects.create(user=request.user)
            messages.success(request, "Your order is on the way.")
            return redirect('home')
        order.is_paid = True
        order.save(update_fields=['is_paid'])
        context = {
            'order_list': order,
            'cartItems': order.cartItems.all(),
            'order_detail': OrderDetail.objects.get(order=order),
        }
        response = render(request, 'ordering/step_3.html', context)
        Order.objects.create(user=request.user, is_paid=False)
        return response


def UpdateCarts(request):
    if request.is_ajax() and request.method == 'POST':
        item_id = request.POST["item_id"]
        item_mode = request.POST["item_mode"]
        order = Order.objects.get_or_create(user=request.user, is_paid=False)[0]
        item = Item.objects.get(id=item_id)
        cart_item = CartItem.objects.filter(order=order, item=item)

        if order.restaurant is None:
            order.restaurant = item.menu.restaurant
            order.restaurant.save()
        elif order.restaurant != item.menu.restaurant:
            return JsonResponse({"errorMsg": f"This item does not belong to '{order.restaurant}'"})

        cart_item = cart_item.first() if cart_item.exists() else CartItem(order=order, item=item)
        quantity = cart_item.Add() if item_mode == "+" else cart_item.Remove() or 0
        data = {
            "quantity": quantity,
            "total_price": cart_item.total_price,
        }
        return JsonResponse(data)
