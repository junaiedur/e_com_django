from django.contrib import admin
from .models import Coupon
from carts.models import Cart , CartItem, Coupon
from carts.admin import CartAdmin , CartItemAdmin
# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percentage','valid_from', 'valid_to', 'active','max_uses', 'used_count', 'is_valid']
    search_fields = ['code']
    list_filter = ['active', 'valid_from', 'valid_to']
    ordering = ['-valid_from',]
admin.site.register(Coupon,CouponAdmin)
