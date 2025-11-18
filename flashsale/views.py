from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import FlashSale

def flash_sale(request):
    sales = FlashSale.objects.filter(is_active=True)
    return render(request, 'sale/flashsales.html', {'sales': sales})
