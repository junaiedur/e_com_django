from django.db import models
from store.models import Product

class BestDeal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255, blank=True)
    discount_percentage = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title