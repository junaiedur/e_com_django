from django.contrib import admin
# from .models import Coupon

# # Register your models here.

# class CouponAdmin(admin.ModelAdmin):
#     list_display = ['code', 'discount_type', 'discount_percentage', 'fixed_discount_amount', 'max_discount_amount', 'valid_from', 'valid_to', 'active','max_uses', 'used_count', 'is_valid'] # নতুন ফিল্ডগুলো যোগ করা হয়েছে
#     search_fields = ['code']
#     list_filter = ['active', 'valid_from', 'valid_to', 'discount_type'] # discount_type যোগ করা হয়েছে
#     ordering = ['-valid_from',]
# admin.site.register(Coupon,CouponAdmin)