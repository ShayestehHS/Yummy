from django.contrib import admin
from django.contrib.auth.models import Group

from Users.models import Driver, User

########################## Register
admin.site.register(User)
admin.site.unregister(Group)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_filter = ('motorbike', 'student', 'driver_lic', 'mobile')
    list_display = ('user', 'phone_number',)
