

# Register your models here.
from django.contrib import admin
from .models import  Supplier, Category, PackagingType, Drug, Stock, Alert,CustomUser,Sale,SaleItem

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'email')
    search_fields = ('name', 'email')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class PackagingTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic_name', 'brand_name', 'batch', 'category', 'packaging_type', 'quantity', 'unit_price', 'expiry_date', 'supplier')
    list_filter = ('category', 'packaging_type', 'expiry_date', 'supplier')
    search_fields = ('name', 'generic_name', 'brand_name', 'batch')

class StockAdmin(admin.ModelAdmin):
    list_display = ('drug', 'quantity', 'last_updated')
    search_fields = ('drug__name',)
    list_filter = ('last_updated',)

# class SaleAdmin(admin.ModelAdmin):
#     list_display = ('drug', 'quantity', 'sale_date', 'total_price')
#     search_fields = ('drug__name',)
#     list_filter = ('sale_date',)

class AlertAdmin(admin.ModelAdmin):
    list_display = ('drug', 'alert_date', 'message')
    search_fields = ('drug__name',)
    list_filter = ('alert_date',)

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PackagingType, PackagingTypeAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Stock, StockAdmin)
# admin.site.register(Sale, SaleAdmin)
admin.site.register(Alert, AlertAdmin)
admin.site.register(CustomUser)
admin.site.register(Sale)
admin.site.register(SaleItem)


# admin.py

