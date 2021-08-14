from django.contrib import admin

from Menu.models import Menu, Item


class ItemInline(admin.StackedInline):
    model = Item
    max_num = 25
    min_num = 1


@admin.register(Menu)
class AdminItem(admin.ModelAdmin):
    inlines = [ItemInline]
