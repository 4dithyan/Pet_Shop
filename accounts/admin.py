from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'email')}),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city')
    search_fields = ('user__username', 'city')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
