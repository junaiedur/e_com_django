from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Variation
from django.db.models import Q
from category.models import Category 
from carts.views import _cart_id
from carts.models import CartItem, Cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from order.models import Order, OrderProduct
from reviews.models import Review
from django.db.models import Q, Min, Max 
# Create your views here.
# def store(request, category_slug=None):
#     categories = None
#     products = None # 11-13-2025
#     if category_slug != None:
#         categories = get_object_or_404(Category, slug=category_slug)
#         products = Product.objects.filter(category=categories, is_available=True) # 11-13-2025
#         paginator = Paginator(products, 2)
#         page = request.GET.get('page')
#         paged_products = paginator.get_page(page)
#         product_count = products.count()
#     else:
#         products = Product.objects.all().filter(is_available=True).order_by('id')
#         paginator = Paginator(products, 5)
#         page = request.GET.get('page')
#         paged_products = paginator.get_page(page)
#         product_count = products.count()
#     context = {
#         'products': paged_products,
#         'product_count': product_count,
#     }
#     return render(request, 'store/store.html', context)

def store(request, category_slug=None):
    categories = None

    # সব available প্রোডাক্ট
    products = Product.objects.filter(is_available=True)

    # যদি category থাকে, আগে সেটা দিয়ে ফিল্টার
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=categories)

    # ====== ফিল্টার প্যারামিটারগুলো নেওয়া ======
    selected_size = request.GET.get('size')
    selected_color = request.GET.get('color')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # size ফিল্টার
    if selected_size:
        products = products.filter(
            variation__variation_category='size',
            variation__variation_value=selected_size,
            variation__is_active=True,
        )

    # color ফিল্টার
    if selected_color:
        products = products.filter(
            variation__variation_category='color',
            variation__variation_value=selected_color,
            variation__is_active=True,
        )

    # price ফিল্টার
    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # variation থেকে ডুপ্লিকেট প্রোডাক্ট যেন না আসে
    products = products.distinct()

    # ====== সাইডবারে দেখানোর জন্য available size / color লিস্ট ======
    available_sizes = Variation.objects.filter(
        variation_category='size',
        is_active=True,
        product__is_available=True,
    ).values_list('variation_value', flat=True).distinct()

    available_colors = Variation.objects.filter(
        variation_category='color',
        is_active=True,
        product__is_available=True,
    ).values_list('variation_value', flat=True).distinct()

    # ====== ডায়নামিক price range (min / max) ======
    base_price_qs = Product.objects.filter(is_available=True)
    if category_slug is not None:
        base_price_qs = base_price_qs.filter(category=categories)

    price_stats = base_price_qs.aggregate(
        price_min=Min('price'),
        price_max=Max('price'),
    )
    price_min = price_stats['price_min']
    price_max = price_stats['price_max']

    # ====== Pagination ======
    if category_slug is not None:
        per_page = 2
    else:
        per_page = 5

    paginator = Paginator(products, per_page)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'available_sizes': available_sizes,
        'available_colors': available_colors,
        'price_min': price_min,
        'price_max': price_max,
        'selected_size': selected_size,
        'selected_color': selected_color,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
    }
    return render(request, 'store/store.html', context)



#search diye kojar jnno use korteci
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


# def product_detail(request, category_slug, product_slug):
#     try:
#         single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
#         in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
#     except Exception as e:
#         raise e

#     if request.user.is_authenticated:
#         try:
#             order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
#         except OrderProduct.DoesNotExist:
#             order_product = None
#     else:
#         order_product = None

#     # 👉 এখানে রিভিউ গুলো নিন
#     reviews = Review.objects.filter(product_id=single_product.id, status=True).order_by('-created_at')

#     context = {
#         'single_product': single_product,
#         'in_cart': in_cart,
#         'orderproduct': order_product,
#         'reviews': reviews,   # 👉 টেমপ্লেটে পাঠালাম
#     }
#     return render(request, 'store/product_detail.html', context)
from django.shortcuts import render, get_object_or_404
from carts.views import _cart_id
from carts.models import CartItem
from order.models import OrderProduct
from reviews.models import Review
from .models import Product


def product_detail(request, category_slug, product_slug):
    # প্রোডাক্ট না পেলে সরাসরি 404
    single_product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
    )

    # কার্টে আছে কিনা
    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request),
        product=single_product
    ).exists()

    # এই ইউজার আসলে প্রোডাক্টটা কিনেছে কিনা (তখনই রিভিউ দেওয়ার সুযোগ)
    if request.user.is_authenticated:
        order_product = OrderProduct.objects.filter(
            user=request.user,
            product_id=single_product.id
        ).exists()
    else:
        order_product = None

    # এই প্রোডাক্টের অ্যাপ্রুভড রিভিউ তালিকা (নতুনটা আগে)
    reviews = Review.objects.filter(
        product=single_product,
        status=True
    ).order_by('-created_at')

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': order_product,
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)

def hot_deals(request):
    products = Product.objects.filter(is_available=True).order_by('-created_date')[:3]
    context = {
        'products': products,
    }
    return render(request, 'store/hot_deals.html', context)