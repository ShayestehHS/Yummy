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
        sum_items = 0
        for cart_item in self.cartItems.all():
            sum_items += (cart_item.item.price * cart_item.quantity)
        try:
            if self.orderdetail.delivery_method == "Delivery":
                sum_items += self.restaurant.delivery_charge
        except OrderDetail.DoesNotExist:
            pass
        self.payout = sum_items

    def save(self, *args, **kwargs):

        if self.cartItems.filter(Q(quantity__gt=0)).values_list('item').count() > 0:
            self.sum_payout()

        self.full_clean()
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
    telephone = models.PositiveIntegerField()
    full_address = models.CharField(max_length=120,
                                    help_text='Maximum length is 120')
    postal_code = models.PositiveIntegerField()
    delivery_day = models.CharField(choices=dayOption, max_length=8)
    delivery_time = models.CharField(max_length=5)
    delivery_method = models.CharField(max_length=8, choices=deliveryOption)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.order.__str__()

    def save(self, *args, **kwargs):
        if self.delivery_method == "Delivery":
            self.order.save()

        self.full_clean()
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
        self.full_clean()
        super(CartItem, self).save(*args, **kwargs)
        self.order.save()

        if self.quantity == 0:
            self.delete()

    def __str__(self):
        return self.item.name
