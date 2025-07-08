from django.contrib import admin
from.models import Cart, CartItem
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display =('cart_id','date_added', 'coupon', 'discount')
    list_filter = ('date_added', 'user')
    search_fields = ('cart_id', 'user__email')

class CartItemAdmin (admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active', 'get_variations')
    list_filter = ('is_active', 'user')
    search_fields = ('product__product_name', 'user__email')
    
    def get_variations(self, obj):
        return ", ".join([str(v) for v in obj.variations.all()])
    get_variations.short_description = 'Variations'

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)

##ai code gula sob deep seek teke neya:
"""from django.contrib import admin
from .models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user', 'date_added', 'coupon', 'discount')
    list_filter = ('date_added', 'user')
    search_fields = ('cart_id', 'user__email')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'cart', 'quantity', 'is_active', 'get_variations')
    list_filter = ('is_active', 'user')
    search_fields = ('product__product_name', 'user__email')

    def get_variations(self, obj):
        return ", ".join([str(v) for v in obj.variations.all()])
    get_variations.short_description = 'Variations'

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
"""
###end