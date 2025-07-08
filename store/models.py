from django.db import models
from category.models import Category , SubCategory, SubSubCategory
from django.urls import reverse
# from ckeditor.fields import RichTextField
# অথবা SubCategory বা Category


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
 # ... অন্যান্য ফিল্ড ...
    # অথবা subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.CharField(max_length=500, unique=True)
    # detail=RichTextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=1, related_name='store_products_by_subcategory')
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.CASCADE, default=1, related_name='store_products_by_subsubcategory') # Unique related_name
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    # def get_url(self):
    #     if self.subcategory and self.subsubcategory:
    #         return reverse('product_detail', args=[self.category.slug, self.subcategory.slug, self.subsubcategory.slug, self.slug])
    #     elif self.subcategory:
    #         # If only subcategory exists, maybe a different URL pattern?
    #         # Example: return reverse('product_detail_by_subcategory', args=[self.category.slug, self.subcategory.slug, self.slug])
    #         return reverse('product_detail', args=[self.category.slug, self.subcategory.slug, 'no-subsub', self.slug]) # Placeholder or specific URL
    #     else:
    #         # If only category exists
    #         # Example: return reverse('product_detail_by_category', args=[self.category.slug, self.slug])
    #         return reverse('product_detail', args=[self.category.slug, self.subcategory.slug, self.subsubcategory.slug, self.slug])
    def get_url(self):
        try:
            if self.subsubcategory:
                return reverse('product detail',args=[
                    self.subsubcategory.sub_category.category.slug,
                    self.subsubcategory.sub_category.slug,
                    self.subsubcategory.slug,
                    self.slug
                ])
            elif self.subcategory:
                return reverse('products_by_subcategory', args=[
                    self.subcategory.category.slug,
                    self.subcategory.slug,
                    self.slug
                ])
            elif self.category:
                return reverse('products_by_category', args=[
                    self.category.slug,
                    self.slug
                ])
            
            return reverse('product_detail_generic', args=[self.slug])
        except Exception:
            return '#'

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