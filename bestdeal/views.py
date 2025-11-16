from django.shortcuts import render, get_object_or_404
from .models import BestDeal
from store.models import Product
# Create your views here.

def best_deals(request):
    best_deals = BestDeal.objects.filter(is_active=True)
    
    best_deal_products = Product.objects.filter(
        id__in=best_deals.values_list('product_id', flat=True),
        is_available=True
    )
    
    context = {
        'best_deals': best_deals,
        'best_deal_products': best_deal_products,
    }
    return render(request, 'bestdeals.html', context)