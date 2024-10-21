from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from store.models import Product
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)# coupon ar code all time kintu unique hobe
    #discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    # (max_digits=5) aita kintu change korte parbo akn coupon code a 5 ta value asbe tai amara akn a aita dilam
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    valid_from = models.DateTimeField()  # coupon validity jedin suru hobe seitar date
    valid_to = models.DateTimeField()  # coupon validity jedin ses hobe seitar date
    active = models.BooleanField(default=True)  # Is the coupon active?

    #specific kono product a coupon code apply ar jnno nicher line a likhbo
    # applicable_products = models.ManyToManyField(Product, related_name='coupons')

    class Meta:
        verbose_name = 'Coupon Code'

    def __str__(self):
        return self.code

    def is_valid(self):
        """
        Check if the coupon is currently valid.
        """
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to