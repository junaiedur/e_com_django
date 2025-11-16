from django.db import models

# Create your models here.

class BestDeal(models.Model):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    discount_percentage = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', '-created_date']
    
    def __str__(self):
        return self.title