from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Wishlist

@login_required
def wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"items": items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect("wishlist")

@login_required
def remove_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect("wishlist")
