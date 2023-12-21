from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'name', 'is_superadmin', 'is_admin', 'is_tksk')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_superadmin', 'is_admin', 'is_tksk')}),
        ('Personal info', {'fields': ('name','location')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name','location', 'is_superadmin', 'is_admin', 'is_tksk')}),
    )
admin.site.register(User, CustomUserAdmin)