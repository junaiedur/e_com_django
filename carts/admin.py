from django.contrib import admin
from.models import Cart, CartItem, Coupon, DeliveryMethod, UsedCoupon
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display =('cart_id','date_added')
    # list_filter = ('date_added', 'user')
    # search_fields = ('cart_id', 'user__email')

class CartItemAdmin (admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')
    # list_filter = ('is_active', 'user')
    # search_fields = ('product__product_name', 'user__email')
    
    # def get_variations(self, obj):
    #     return ", ".join([str(v) for v in obj.variations.all()])
    # get_variations.short_description = 'Variations'
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'max_usage', 'used_count', 'is_active')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code',)

class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'estimated_days', 'is_active')
    list_filter = ('is_active',)

class UsedCouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'used_at')
    list_filter = ('used_at',)

class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_display_info', 'estimated_days', 'is_active')
    list_filter = ('is_active', 'is_free_delivery')
    list_editable = ('price', 'is_active')
    
    def get_display_info(self, obj):
        if obj.is_free_delivery:
            return f"Free (Min order: {obj.min_order_amount} Tk)"
        return f"{obj.price} Tk"
    get_display_info.short_description = 'Delivery Charge'

admin.site.register(Coupon, CouponAdmin)
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
admin.site.register(UsedCoupon, UsedCouponAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)