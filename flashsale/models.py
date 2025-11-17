
from django.db import models
from store.models import Product

class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.product.product_name
