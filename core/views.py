from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from bestdeal.models import BestDeal 

from store.models import SubBanner

from store.models import SubBanner

def home(request):
    sub_banners = SubBanner.objects.all()
    best_deals = BestDeal.objects.filter(is_active=True)
    best_deal_products = [deal.product for deal in best_deals]

    context = {
        'sub_banners': sub_banners,
    }
    return render(request, 'index.html', context)
