from django.contrib import admin
from .models import ProductCategory, Product, InventoryLog


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


class InventoryLogInline(admin.TabularInline):
    model = InventoryLog
    extra = 0
    can_delete = False
    readonly_fields = ['change_type', 'quantity_change', 'previous_quantity', 'new_quantity', 'reason', 'created_by', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_low_stock', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    inlines = [InventoryLogInline]
    
    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'


@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ['product', 'change_type', 'quantity_change', 'previous_quantity', 'new_quantity', 'created_at']
    list_filter = ['change_type', 'created_at']
    search_fields = ['product__name', 'reason']
    readonly_fields = ['created_at']
