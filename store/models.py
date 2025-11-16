from django.db import models
from category.models import Category 
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    discount_price = models.IntegerField(null=True, blank=True)  # Flash Sale
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)  # Admin Feature
    views = models.IntegerField(default=0)  # Popular Products
    cart_added = models.IntegerField(default=0)  # Popular Products

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
#sub banner
class SubBanner(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title
