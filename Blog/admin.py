from django.contrib import admin

from Blog.models import Blog, XtdComment
from Users.models import User


########################## Filter
class OwnerFilter(admin.SimpleListFilter):
    title = "Author"
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = User.objects.filter(blog__isnull=False).distinct()
        return ((author.username, author.username) for author in authors)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author__username=self.value())


########################## Action
@admin.action(description="Change Approved")
def change_approved(modeladmin, request, queryset):  # action => Restaurant
    qs = queryset[0]  # Get blog object
    if qs.is_approved:
        queryset.update(is_approved=False)
    else:
        queryset.update(is_approved=True)


########################## Register
admin.site.register(XtdComment)


@admin.register(Blog)
class RestaurantAdmin(admin.ModelAdmin):
    list_filter = ('is_approved', 'is_primary', OwnerFilter)
    list_display = ('title', 'author','is_approved')
    actions = [change_approved,]
