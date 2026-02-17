from django.contrib import admin
from .models import Category, Pet

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'category', 'price', 'age_months', 'is_available', 'is_vaccinated')
    list_filter = ('category', 'is_available', 'is_vaccinated', 'gender')
    search_fields = ('name', 'breed', 'description')
    list_editable = ('is_available',)
