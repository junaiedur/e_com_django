from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product, SubCategory, SubSubCategory # Assuming you have a Product model



from .models import SubSubCategory # অথবা SubCategory বা Category

class Product(models.Model):
    # ... অন্যান্য ফিল্ড ...
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    # অথবা subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    # অথবা category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)


# Create your views here.
def home(request):
    return render(request,'index.html')


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    # Assuming you have a Product model linked to Category or SubCategory
    # products = Product.objects.filter(category=category)
    # Or if products are linked to subcategories, you'd fetch them differently
    context = {
        'category': category,
        # 'products': products,
    }
    return render(request, 'store.html', context)

def products_by_subcategory(request, category_slug, subcategory_slug, subsubcategory_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(SubCategory, category=category, slug=subcategory_slug)
    subsubcategory = get_object_or_404(SubSubCategory, sub_category=subcategory, slug=subsubcategory_slug)
    # Assuming you have a Product model linked to SubCategory
    # products = Product.objects.filter(subcategory=subcategory)
    context = {
        'category': category,
        'subcategory': subcategory,
        'subsubcategory': subsubcategory,
        # 'products': products,
    }
    return render(request, 'store.html', context)