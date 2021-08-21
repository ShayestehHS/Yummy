from django.db import models
from django.db.models import Q

from Menu.models import Item
from Users.models import User
from Yummy.models import Restaurant


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    payout = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def sum_payout(self):
        sumItems = 0
        for cart_item in self.cartItems.all():
            sumItems += (cart_item.item.price * cart_item.quantity)
        try:
            if self.orderdetail.deliveryMethod == "Delivery":
                sumItems += self.restaurant.delivery_charge
        except OrderDetail.DoesNotExist:
            pass
        self.payout = sumItems

    def save(self, *args, **kwargs):
        if self.cartItems.filter(Q(quantity__gt=0)).values_list('item').count() > 0:
            self.sum_payout()

        super(Order, self).save(*args, **kwargs)


class OrderDetail(models.Model):
    dayOption = [
        ('Today', 'Today'),
        ('Tomorrow', 'Tomorrow'),
    ]
    deliveryOption = [
        ('Delivery', 'Delivery'),
        ('TakeAway', 'TakeAway'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    telephone = models.PositiveIntegerField(null=True)
    full_address = models.CharField(max_length=120, null=True)
    postal_code = models.PositiveIntegerField(null=True)
    deliveryDay = models.CharField(choices=dayOption, max_length=8, null=True)
    deliveryTime = models.CharField(max_length=7, null=True)
    deliveryMethod = models.CharField(max_length=8, choices=deliveryOption, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.order.__str__()

    def save(self, *args, **kwargs):
        if self.deliveryMethod == "Delivery":
            self.order.save()
        super(OrderDetail, self).save(*args, **kwargs)


class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='cartItems')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    total_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def Add(self):
        self.quantity += 1
        self.total_price += self.item.price
        self.save()
        return self.quantity

    def Remove(self):
        self.quantity -= 1
        self.total_price -= self.item.price
        self.save()
        return self.quantity

    def save(self, *args, **kwargs):
        super(CartItem, self).save(*args, **kwargs)
        self.order.save()
        if self.quantity == 0:
            self.delete()

    def __str__(self):
        return self.item.name
