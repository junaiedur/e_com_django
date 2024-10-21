from django.db import models
from store.models import Product, Variation
from accounts.models import Account
from Coupon.models import Coupon

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.cart_id

    def get_total_price(self):
        total = sum(item.sub_total() for item in self.cart_items.all())

        if self.coupon:
            total -= total * (self.coupon.discount_percentage / 100)
        return total - self.discount


class CartItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product


