from django.contrib import admin
from .models import FlashSale

class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_price', 'is_active', 'start_time', 'end_time')
    list_filter = ('is_active',)

admin.site.register(FlashSale, FlashSaleAdmin)
