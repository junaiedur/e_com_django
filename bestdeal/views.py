from django.shortcuts import render
from .models import BestDeal
from store.models import Product
from category.models import Category

def best_deals(request):
    deals = BestDeal.objects.filter(is_active=True).select_related("product").order_by("display_order")
    
    products = Product.objects.filter(
        id__in=deals.values_list("product_id", flat=True),
        is_available=True
    )
      # For easy matching in template
    deal_map = {deal.product_id: deal for deal in deals}
    context = {
         "best_deal_products": products,
        "deal_map": deal_map,
        "popular_categories": Category.objects.all(),
    }

    return render(request, "sale/bestdeals.html", context)
