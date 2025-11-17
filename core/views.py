from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

from store.models import SubBanner

from store.models import SubBanner

def home(request):
    sub_banners = SubBanner.objects.all()

    context = {
        'sub_banners': sub_banners,
    }
    return render(request, 'index.html', context)
