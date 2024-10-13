from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at')
    # prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('payment_id',)

class OrderAdmin(admin.ModelAdmin):
    list_display =('user','first_name', 'payment', 'email', 'address_line_1','status','is_ordered','updated_at')
    list_editable = ('is_ordered',)
    # list_filter =['product', 'variation_value', 'created_date']

class OrderProductAdmin(admin.ModelAdmin):
    list_display =('order','payment', 'user', 'quantity', 'product_price', 'updated_at')
    list_editable = ('product_price',)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
