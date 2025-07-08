from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, SubCategory, SubSubCategory # Assuming you have a Product model
from .models import models
from store.models import Product


# Create your views here.
def home(request):
    return render(request,'index.html')


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'store/store.html', context)

def products_by_subcategory(request, category_slug, subcategory_slug, subsubcategory_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(SubCategory, category=category, slug=subcategory_slug)
    # subsubcategory = get_object_or_404(SubSubCategory, sub_category=subcategory, slug=subsubcategory_slug)
    products = Product.objects.filter(subcategory=subcategory)
    context = {
        'category': category,
        'subcategory': subcategory,
        'products': products,
    }
    return render(request, 'store/store.html', context)

def products_by_subsubcategory(request, category_slug, subcategory_slug, subsubcategory_slug):
    category = get_object_or_404(category, slug=category_slug)
    subcategory = get_object_or_404(SubCategory, category=category, slug=subcategory_slug)
    subsubcategory = get_object_or_404(SubSubCategory, sub_category=subcategory, slug=subsubcategory_slug)
    products = Product.objects.filter(subsubcategory=subsubcategory)
    context = {
        'category': category,
        'subcategory': subcategory,
        'subsubcategory': subsubcategory,
        'products': products,
    }
    return render(request, 'store/store.html')




def product_detail(request, product_slug, category_slug=None, subcategory_slug=None, subsubcategory_slug=None):
    product = get_object_or_404(Product, slug=product_slug)
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)