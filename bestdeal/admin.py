from django.contrib import admin
from .models import BestDeal

# Register your models here.

@admin.register(BestDeal)
class BestDealAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'discount_percentage', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('title', 'product__product_name')