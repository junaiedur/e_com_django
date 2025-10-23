from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'quantity', 'product_price', 'ordered']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =['order_number','full_name','payment', 'email', 'status','is_ordered','updated_at']
    # list_editable = ['is_ordered']
    list_filter = ['status', 'is_ordered', 'created_at']
    # list_filter =['product', 'variation_value', 'created_date']
    search_fields = ['order_number', 'full_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
    # def has_add_permission(self, request, obj=None):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'product_price', 'ordered']
    list_filter = ['ordered', 'created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['payment_id', 'user__email', 'mobile_number']
