from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'quantity', 'product_price', 'ordered']
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    list_display =['order_number','full_name','payment', 'email', 'status','is_ordered','updated_at']
    # list_editable = ['is_ordered']
    list_filter = ['status', 'is_ordered']
    # list_filter =['product', 'variation_value', 'created_date']
    search_fields = ['order_number', 'full_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
    # def has_add_permission(self, request, obj=None):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False

# class OrderProductAdmin(admin.ModelAdmin):
#     list_display =('order','payment', 'user', 'quantity', 'product_price', 'updated_at')
#     list_editable = ('product_price',)
# admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)