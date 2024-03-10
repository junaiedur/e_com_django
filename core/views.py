from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product


# Create your views here.
def home(request):
    products = Product.objects.all().filter(is_available=True) #akna filter debar karon ai je amader product autometic avaialable ace ki nah seta autometic vabe kaj korco
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)
