from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address

# Register your models here.

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    fields = ['recipient_name', 'line1', 'line2', 'city', 'state', 'phone', 'is_default']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'is_active']
    search_fields = ['email', 'username']
    fieldsets = BaseUserAdmin.fieldsets + (("Contact", {'fields': ('phone',)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (("Contact", {'fields': ('phone', 'first_name', 'last_name', 'email',)}),)
    inlines = [AddressInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipient_name', 'line1', 'line2', 'city', 'state', 'phone', 'is_default']
    list_filter = ['state', 'city', 'is_default']
    search_fields = ['state', 'recipient_name', 'phone']
    autocomplete_fields = ['user']
    list_select_related = ['user']