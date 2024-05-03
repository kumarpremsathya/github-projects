from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(Profile)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user_name', 'mobile', 'otp']

    def get_user_name(self, obj):
        return obj.user.first_name if obj.user else ''
    get_user_name.short_description = 'User Name'