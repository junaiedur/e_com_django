from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem, Coupon, DeliveryMethod, UsedCoupon
from store.models import Product , Variation, SubBanner
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order .models import Order, Payment, OrderProduct
import datetime
from django.utils import timezone
from django.conf import settings
# Import your models and forms
from accounts.models import Account
from category.models import Category
from bestdeal.models import BestDeal
# Helper function to get or create a unique cart ID for sessions
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# Add item to cart
def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    product = Product.objects.get(id=product_id) #get the product
    if current_user.is_authenticated:
        product_variation = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

    # if current_user.is_authenticated:
        # User is logged in
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            existing_variations_list = [list(item.variations.all()) for item in cart_items]
            id = []
            for item in cart_items:
                existing_variation = item.variations.all()
                existing_variations_list.append(list(existing_variation))
                id.append(item.id)
        # ids = [item.id for item in cart_items]
            if product_variation in existing_variations_list:
                index = existing_variations_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product, 
                quantity = 1, 
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # User is not logged in
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
             # color = request.POST['color'] #<select name="color"> ja takbe akn tai name dibo['color] 
             # size = request.POST['size']
            # print(color, size):
        # User is not logged in
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        # Check if the cart item already exists
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            print(existing_variation_list)
            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save() 
        else:
            cart_item = CartItem.objects.create(
                product=product, 
                quantity=1, 
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

# remove from cart
def remove_from_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
             cart_item.delete()
    except:
         pass
    return redirect('cart')


def remove(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')

# #cupon start#
# def apply_coupon(request):
#     if request.method == 'POST':
#         coupon_code = request.POST.get('code')
#         try:
#             coupon = Coupon.objects.get(code=coupon_code, is_active=True)
#             cart_total = 0
#             if request.user.is_authenticated:
#                 cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#             else:
#                 cart = Cart.objects.get(cart_id=_cart_id(request))
#                 cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
#             for item in cart_items:
#                 cart_total += (item.product.price * item.quantity)
#             if coupon.is_valid(cart_total):
#                 request.session['coupon_id'] = coupon.id
#                 request.session['coupon_code'] = coupon.code
#                 messages.success(request, 'Coupon applied successfully!')
#             else:
#                 messages.error(request, 'Coupon is not valid or has expired.')
#         except Coupon.DoesNotExist:
#             messages.error(request, 'Coupon does not exist.')
#     return redirect('cart')

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('code')
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None)
            request.session.pop('coupon_code', None)
            messages.error(request, 'Coupon does not exist.')
            return redirect('cart')
        
         # Cart items collect 
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        cart_total = sum([item.product.price * item.quantity for item in cart_items])

        if coupon.is_valid(cart_total):
            request.session['coupon_id'] = coupon.id
            request.session['coupon_code'] = coupon.code
            messages.success(request, 'Coupon applied successfully!')
        else:
            # Invalid হলে session থেকে remove
            request.session.pop('coupon_id', None)
            request.session.pop('coupon_code', None)
            messages.error(request, 'Coupon is not valid or has expired.')
    return redirect('cart')


def remove_coupon(request):
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
    messages.success(request, 'Coupon removed successfully!')
    return redirect('cart')
#cupon end#



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        vat = 0
        total = 0
        total_price = 0
        discount_amount = 0
        delivery_charge = 0
        selected_delivery_method = None

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
           
        vat = (1 * total)/100

        # Apply coupon discount
        coupon_id = request.session.get('coupon_id')
        if coupon_id:
            try:
                coupon = Coupon.objects.get(id=coupon_id)
                if coupon.is_valid(total):
                    discount_amount = coupon.get_discount_amount(total)
                else:
                    request.session.pop('coupon_id', None)
                    request.session.pop('coupon_code', None)
            except Coupon.DoesNotExist:
                request.session.pop('coupon_id', None)
                request.session.pop('coupon_code', None)
# Calculate delivery charge (you can implement more complex logic)
        delivery_method_id = request.session.get('delivery_method_id')
        delivery_methods = DeliveryMethod.objects.filter(is_active=True)

        if delivery_method_id:
            try:
                selected_delivery_method = DeliveryMethod.objects.get(id=delivery_method_id, is_active=True)
                if selected_delivery_method.is_free_delivery and total >= selected_delivery_method.min_order_amount:
                    delivery_charge = 0
                else:
                    delivery_charge = selected_delivery_method.price
            except DeliveryMethod.DoesNotExist:
                try:
                    selected_delivery_method = DeliveryMethod.objects.get(name__icontains="Standard", is_active=True)
                    delivery_charge = selected_delivery_method.price
                    request.session['delivery_method_id'] = selected_delivery_method.id
                
                except DeliveryMethod.DoesNotExist:
                    delivery_charge = 60 

        else:
            try:
                selected_delivery_method = DeliveryMethod.objects.get(name__icontains="Standard", is_active=True)
                delivery_charge = selected_delivery_method.price
                request.session['delivery_method_id'] = selected_delivery_method.id
            except DeliveryMethod.DoesNotExist:

                delivery_charge = 60
         # Convert all values to float before calculation
        total_float = float(total)
        vat_float = float(vat)
        delivery_charge_float = float(delivery_charge)
        discount_amount_float = float(discount_amount)


        total_price = total_float + vat_float + delivery_charge_float - discount_amount_float

    except ObjectDoesNotExist:
        delivery_methods = DeliveryMethod.objects.filter(is_active=True)

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'vat': vat,
        'discount_amount': discount_amount,
        'delivery_charge': delivery_charge, 
        'total_price': total_price,
        'coupon_code': request.session.get('coupon_code', None),
        'delivery_methods': delivery_methods,
        'selected_delivery_method': selected_delivery_method,
    }
    return render(request, 'cart/cart.html', context)

@login_required(login_url='login') #ai line ta use korar karon amra jodi site a login kora nah take tahole amra cart product gula jodi checkout korar time a amake login korte bola hobe 
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        vat = 0
        total_price = 0
        discount_amount = 0
        delivery_charge = 0
        selected_delivery_method = None

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        # totals = total
      
        vat = (1 * total)/100
        # Apply coupon discount
        coupon_id = request.session.get('coupon_id')
        if coupon_id:
            try:
                coupon = Coupon.objects.get(id=coupon_id)
                if coupon.is_valid(total):
                    discount_amount = coupon.get_discount_amount(total)
                else:
                    # Invalid হলে session থেকে remove
                    request.session.pop('coupon_id', None)
                    request.session.pop('coupon_code', None)
            except Coupon.DoesNotExist:
                request.session.pop('coupon_id', None)
                request.session.pop('coupon_code', None)


        delivery_method_id = request.session.get('delivery_method_id')
        delivery_methods = DeliveryMethod.objects.filter(is_active=True)        
        
        if delivery_method_id:
            try:
                selected_delivery_method = DeliveryMethod.objects.get(id=delivery_method_id, is_active=True)
                if selected_delivery_method.is_free_delivery and total >= selected_delivery_method.min_order_amount:
                    delivery_charge = 0
                else:
                    delivery_charge = selected_delivery_method.price
            except DeliveryMethod.DoesNotExist:

                try:
                    selected_delivery_method = DeliveryMethod.objects.get(name__icontains='standard', is_active=True)
                    delivery_charge = selected_delivery_method.price

                except DeliveryMethod.DoesNotExist:
                    delivery_charge = 60
        else:
            try:
                selected_delivery_method = DeliveryMethod.objects.get(name__icontains='standard', is_active=True)
                delivery_charge = selected_delivery_method.price
            except DeliveryMethod.DoesNotExist:
                delivery_charge = 60

         # Convert all values to float before calculation
        total_float = float(total)
        vat_float = float(vat)
        delivery_charge_float = float(delivery_charge)
        discount_amount_float = float(discount_amount)
        # Calculate total price
    
        total_price = total_float + vat_float + delivery_charge_float - discount_amount_float        # Get available delivery methods
        
    except ObjectDoesNotExist:
        delivery_methods = DeliveryMethod.objects.filter(is_active=True)


    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'vat': vat,
        'discount_amount': discount_amount,
        'delivery_charge': delivery_charge,
        'total_price': total_price,
        'delivery_methods': delivery_methods,
        'selected_delivery_method': selected_delivery_method,
        'coupon_code': request.session.get('coupon_code', None),

    }
    return render(request, 'cart/checkout.html',context)

def select_delivery_method(request):
    if request.method == 'POST':
        delivery_method_id = request.POST.get('delivery_method_id')
        if delivery_method_id:
            try:
                delivery_method = DeliveryMethod.objects.get(id=delivery_method_id, is_active=True)
                request.session['delivery_method_id'] = delivery_method.id
                messages.success(request, f'{delivery_method.name} selected successfully!')
            except DeliveryMethod.DoesNotExist:
                messages.error(request, 'Invalid delivery method selected.')
        else:
            try:
                standard_delivery = DeliveryMethod.objects.get(name__icontains='standard', is_active=True)
                request.session['delivery_method_id'] = standard_delivery.id
            except DeliveryMethod.DoesNotExist:
                pass
    return redirect('cart')

from store.models import Product

def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    flash_sale = Product.objects.filter(discount_price__isnull=False, is_available=True)[:4]
    trending = Product.objects.filter(views__gt=10).order_by('-views')[:8]

    # Best Deals (Dynamic)
    best_deals = BestDeal.objects.filter(is_active=True).select_related("product").order_by("display_order")
    best_deal_products = [deal.product for deal in best_deals]

    context = {
        "featured_products": featured_products,
        "sub_banners": SubBanner.objects.all(),
        "flash_sale": flash_sale,
        "trending": trending,
        "popular_categories": Category.objects.all(),

        # Best Deals
        "best_deals": best_deals,
        "best_deal_products": best_deal_products,
    }

    return render(request, "index.html", context)