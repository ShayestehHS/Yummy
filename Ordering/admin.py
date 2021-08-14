from django.contrib import admin

from Ordering.models import Order, CartItem, Item

########################## Register
admin.site.register(Item)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('is_paid',)
    list_display = ("user", "payout", "is_paid")


@admin.register(CartItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("item", "quantity")
