from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating')
    search_fields = ('product__product_name', 'user__email', 'subject')

admin.site.register(Review, ReviewAdmin)
