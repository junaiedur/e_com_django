from django.db import models
from django.urls import reverse


# Create your models here
class Category(models.Model):

    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True) #blank= True aita debar mane hocce aita optional tai
    category_images = models.ImageField(upload_to='photos/categories', blank=True)

#amder jodi admin panela kono name r banan vul ase se ketre amra ai vabe chane korbo:
    class Meta:
        verbose_name = 'category' # akn a amr app ar name
        verbose_name_plural = 'categories' # akn a ami je nai solve kora dite chai seta

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])


    def __str__(self):
        return self.category_name


