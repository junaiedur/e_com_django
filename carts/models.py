from django.db import models 
from store.models import Product, Variation
from accounts.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.utils import timezone
from category.models import Category
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

 
class CartItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        # if self.quantity is not None and self.product.price is not None:
        return self.product.price * self.quantity
        # else:
            # return 0 
    def __unicode__(self):
        return self.product

# New models for Coupon and Delivery
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_usage = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self, order_total=0):
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_to and 
                self.used_count < self.max_usage and
                order_total >= self.min_order_amount)
    
    def get_discount_amount(self, order_total):
        if self.discount_type == 'percentage':
            return (self.discount_value * order_total) / 100
        else:
            return min(self.discount_value, order_total)
    
    def __str__(self):
        return self.code


class DeliveryMethod(models.Model): 
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    estimated_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_free_delivery = models.BooleanField(default=False)
    min_order_amount  = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
    def get_display_price(self, cart_total=0):
        if self.is_free_delivery and cart_total >= self.min_order_amount:
            return "FREE"
        return f"{self.price} Tk"


class UsedCoupon(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, null=True)
    
    class Meta:
        unique_together = ('user', 'coupon')

