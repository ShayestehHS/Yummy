from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.html import format_html

from Yummy.models import Restaurant, RestaurantImage, OpeningTime, RestaurantReview


########################## Stack inline
class RestaurantImageAdmin(admin.StackedInline):
    model = RestaurantImage
    min_num = 3
    max_num = 16


class RestaurantOpeningTime(admin.StackedInline):
    model = OpeningTime
    max_num = 7
    min_num = 7
    can_delete = False


########################## Action
@admin.action(description="Change popular")  # action => Restaurant
def change_popular(modeladmin, request, queryset):
    qs = queryset[0]  # Get restaurant object
    if qs.is_popular:
        queryset.update(is_popular=False)
    else:
        queryset.update(is_popular=True)


@admin.action(description="Change delivery")
def change_delivery(modeladmin, request, queryset):  # action => Restaurant
    qs = queryset[0]  # Get restaurant object
    if qs.is_delivery:
        queryset.update(is_delivery=False)
    else:
        queryset.update(is_delivery=True)


@admin.action(description="Change TakeAway")
def change_take_away(modeladmin, request, queryset):  # action => Restaurant
    qs = queryset[0]  # Get restaurant object
    if qs.is_delivery:
        queryset.update(is_take_away=False)
    else:
        queryset.update(is_take_away=True)


########################## Register
admin.site.register(RestaurantReview)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        """
            This function show logo of restaurant
            if obj.logo == None
                show default
        """
        if obj.logo:
            return format_html(
                f'<img src="{obj.logo.url}" style="width: 50px;height: 50px" alt="logo of {obj.name}" />')
        else:
            return format_html(
                f'<img src="/media/Restaurant/133%20restaurant/thumb_restaurant.jpg" style="width: 50px;height: 50px" alt="logo of {obj.name}" />')

    def Owner(self, obj):
        """
        This function
        'create link of owner'
        and
        'show the username of owner'
        in
        display_list
        """
        if obj.owner:
            return format_html(
                f'<a href="http://127.0.0.1:8000/admin/Users/user/{obj.owner.id}/change/">{obj.owner.username}</a>')
        else:
            return 'None'

    class Meta:
        model = Restaurant

    image_tag.short_description = 'logo'
    inlines = [RestaurantImageAdmin, RestaurantOpeningTime]
    actions = [change_delivery, change_popular, change_take_away]
    image_tag.short_description = 'logo'
    list_display = ['image_tag', 'name', 'Owner', 'is_popular', 'is_take_away', 'is_delivery']
    list_display_links = ['image_tag', 'name']
    ordering = ['name']
    search_fields = ['name']
    list_filter = ['is_submit', 'is_popular', 'is_take_away', 'is_delivery']
    readonly_fields = ['rating',]


########################## Unregister
admin.site.unregister(Site)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(EmailAddress)
