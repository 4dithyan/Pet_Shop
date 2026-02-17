from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_item_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'comment')
    
    def get_item_name(self, obj):
        return obj.product.name if obj.product else obj.pet.name if obj.pet else 'N/A'
    get_item_name.short_description = 'Item'
