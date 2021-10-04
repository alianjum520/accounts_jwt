from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


# Register your models here.

class UserAdmin(BaseUserAdmin):

    """
    This class is used to customize django admin panel for users model(table)
    to add different columns in table for readiability
    """

    list_display = ['email','username', 'first_name', 'last_name', 'is_staff','is_active']
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', )


admin.site.register(User, UserAdmin)
