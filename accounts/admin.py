from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.

class UserAdmin(BaseUserAdmin):

    list_display = ['email','username', 'first_name', 'last_name', 'is_staff','is_active']
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', )


admin.site.register(User, UserAdmin)