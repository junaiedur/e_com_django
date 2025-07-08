from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem
from store.models import Product , Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Coupon.forms import ApplyCouponForm
from Coupon.models import Coupon 
from order .models import Order, Payment, OrderProduct
import datetime
from django.utils import timezone
from store.models import Product

# # Define a fixed delivery charge
# DELIVERY_CHARGE = 50.00 # Example: Tk 

# # # Create your views here.
# def _cart_id(request):
#     cart = request.session.session_key
#     if not cart:
#         cart = request.session.create()
#     return cart



# # # Helper function to handle adding items to cart gpt start
# def _handle_cart_item(cart_item, product_variation):
#     if product_variation in cart_item['existing_variation_list']:
#         index = cart_item['existing_variation_list'].index(product_variation)
#         item_id = cart_item['id'][index]
#         item = CartItem.objects.get(product=cart_item['product'], id=item_id)
#         item.quantity += 1
#         item.save()
#     else:
#         item = CartItem.objects.create(
#             product=cart_item['product'], 
#             quantity=1, 
#             user=cart_item['user'], 
#             cart=cart_item.get('cart', None)
#         )
#         if product_variation:
#             item.variations.clear()
#             item.variations.add(*product_variation)
#         item.save()
# # Helper function to handle adding items to cart gpt end

#     # add to cart
# def add_cart(request, product_id):
#     current_user = request.user
#     product = Product.objects.get(id=product_id)#get the product
    
#     product_variation = [] #gpt teke niye ami akn aai line ta diyeci
#     # if user is not authenticated
#     if current_user.is_authenticated:
#         product_variation = [] #ai line ta hide korci karon gpt akn a ai code dai nai opore diyece
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except:
#                     pass
#         # color = request.POST['color'] #<select name="color"> ja takbe akn tai name dibo['color] 
#         # size = request.POST['size']
#         # print(color, size)

#         #msg
#         messages.success(request, "product added successfully")
#         is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        
#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product , user=current_user)
#             # existing variation -> database
#             # carrent variation -> product_variation
#             # item_id -> database
#             existing_variation_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 existing_variation_list.append(list(existing_variation))
#                 id.append(item.id)
#             # print(existing_variation_list)

#             if product_variation in existing_variation_list:
#                 index = existing_variation_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()

#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, user=current_user)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()

#         else:
#             cart_item = CartItem.objects.create(
#                 product = product,
#                 quantity = 1,
#                 user = current_user,
#             )
#             if len (product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart')

#     # if user is not authenticated
#     else:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except:
#                     pass
#             # color = request.POST['color'] #<select name="color"> ja takbe akn tai name dibo['color] 
#             # size = request.POST['size']
#             # print(color, size)

        
#         try:
#             cart = Cart.objects.get(cart_id= _cart_id(request)) #get the cart using the cart_id present in the session
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(
#                 cart_id = _cart_id(request)
#             )
#         cart.save()

#         is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product , cart=cart)
#             existing_variation_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 existing_variation_list.append(list(existing_variation))
#                 id.append(item.id)
#             print(existing_variation_list)

#             if product_variation in existing_variation_list:
#                 index = existing_variation_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()

#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()

#         else:
#             cart_item = CartItem.objects.create(
#                 product = product,
#                 quantity = 1,
#                 cart = cart,
#             )
#             if len (product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart')

# #remove from cart
# def remove_from_cart(request, product_id, cart_item_id):
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()
#     except:
#         pass
#     return redirect('cart')

# # remove or delete cart

# def remove(request,product_id, cart_item_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.user.is_authenticated:
#         cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#     else:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
#     cart_item.delete()
#     return redirect('cart')

# def cart(request, total=0, quantity=0, cart_items=None):
#     try:
#         vat = 0
#         total = 0
#         total_price = 0
#         #discount_amount = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
           
#         vat = (1 * total)/100
#         total_price = total + vat
#         # delevary += 60

#         # Handle coupon application start
#         # if request.method == 'POST':
#         #     code = request.POST.get('coupon_code')
#         #     now = timezone.now()
#         #     try:
#         #         coupon = Coupon.objects.get(code=code, active=True, valid_from__lte=now, valid_to__gte=now)
#         #         applicable_items = cart_items.filter(product__in=coupon.applicable_products.all())
#         #         if applicable_items.exists():
#         #             for item_product in applicable_items:
#         #                 discount_amount = item_product.product.price * (coupon.discount / 100)
#         #                 total_price -= discount_amount
#         #                 item_product.save()
#         #             messages.success(request, f'Coupon "{coupon.code}" applied successfully!')
#         #         # messages.success(request, f'Coupon "{coupon.code}" applied successfully!')

#         #     except Coupon.DoesNotExist:
#         #         messages.error(request, 'Invalid or expired coupon code.')

#         # # Handle coupon application end

#     except ObjectDoesNotExist:
#         pass

#     context = {
#         'cart_items': cart_items,
#         'total': total,
#         'quantity': quantity,
#         'vat': vat,
#         'total_price' : total_price,
#         # 'discount_amount': discount_amount
#         # 'delevary' : delevary,
#     }
#     return render(request, 'cart/cart.html', context)

# #checkout page design:
# @login_required(login_url='login') #ai line ta use korar karon amra jodi site a login kora nah take tahole amra cart product gula jodi checkout korar time a amake login korte bola hobe 
# def checkout(request, total=0, quantity=0, cart_items=None):
#     try:
#         vat = 0
#         total_price = 0
#         totals = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)

#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
        
#         if request.method == 'POST':
#             form = ApplyCouponForm(request.POST)
#             if form.is_valid():
#                 code = form.cleaned_data['code']
#                 now = timezone.now()
                
#                 try:
#                     # Look up the coupon by code and check if it's valid
#                     coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
                    
#                     # Get the user's cart
#                     cart = Cart.objects.get(user=request.user)
#                     cart.coupon = coupon
#                     cart.save()
                    
#                     messages.success(request, 'Coupon applied successfully!')
#                 except Coupon.DoesNotExist:
#                     messages.error(request, 'This coupon does not exist or is invalid.')
#                 return redirect('cart')
#         else:
#             form = ApplyCouponForm()

#         # cart_items = CartItem.objects.filter(user=request.user)
#         # totals = sum(item.sub_total for item in cart_items)
#         # coupon_id = request.session.get('coupon_id')
#         # discount = 0

#         # if coupon_id:
#         #     coupon = get_object_or_404(Coupon, id=coupon_id)
#         #     discount = (coupon.discount / 100) * totals
#         #     totals -= discount

#         # coupon_form = ApplyCouponForm(request.POST)
#         # if coupon_form.is_valid():
#         #     current_time = timezone.now()
#         #     code = coupon_form.cleaned_data.get('code')
#         #     coupon_obj = Coupon.objects.get(code=code, active=True)
#         #     if coupon_obj.valid_to >= current_time:
#         #         get_discount = (coupon_obj.discount / 100) * cart_items.sub_total()
#         #         total_price_after_discount = cart_items.sub_totals() - get_discount
#         #         request.session['discount_total'] = total_price_after_discount
#         #         request.session['coupon_code'] = code
#         #         return redirect('cart')
#         #     else:
#         #         coupon_obj.active = True
#         #         coupon_obj.save()
#         #         return redirect('cart')
#         # total_price_after_discount = request.session.get('discount_total')
#         # coupon_code = request.session.get('coupon_code')


#         vat = (1 * total)/100
#         total_price = total + vat
#         # delevary += 60
#     except ObjectDoesNotExist:
#         pass

#     context = {
#         'cart_items': cart_items,
#         'total': total,
#         'quantity': quantity,
#         'vat': vat,
#         'total_price' : total_price,
#         'totals': totals,
#         # 'discount': discount,
#         # 'coupon_form': coupon_form,
#         # 'coupon_code': coupon_code,
#         # 'total_price_after_discount': total_price_after_discount
#     }
#     return render(request, 'cart/checkout.html',context)

# # @login_required(login_url='login')
# # def checkout(request, total=0, quantity=0, discount = 0, cart_items=None):
# #     try:
# #         vat = 0
# #         discount = 0
# #         total_price = 0

# #         if request.user.is_authenticated:
# #             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
# #         else:
# #             cart = Cart.objects.get(cart_id=_cart_id(request))
# #             cart_items = CartItem.objects.filter(cart=cart, is_active=True)

# #         for cart_item in cart_items:
# #             total += (cart_item.product.price * cart_item.quantity)
# #             quantity += cart_item.quantity
        
# #         # Calculate VAT, if applicable.
# #         vat = total * 0.15  # Example: 15% VAT
# #         total_price = total + vat
        
# #         # Your existing code for handling checkout
# #         coupon_code = request.POST.get('coupon_code')

# #         if coupon_code:
# #             try:
# #                 # Validate the coupon (this assumes you have a Coupon model)
# #                 coupon = Coupon.objects.get(code=coupon_code, is_active=True)
# #                 discount = coupon.discount_amount  # or calculate discount based on percentage
# #                 # Update total price after applying the discount
# #                 total_price -= discount
# #             except Coupon.DoesNotExist:
# #                 messages.error(request, "Invalid coupon code.")

# #         # Pass discount and total_price to the template for display
# #     except ObjectDoesNotExist:
# #         pass

# #     context = {
# #         'cart_items': cart_items,
# #         'total': total,
# #         'quantity': quantity,
# #         'vat': vat,
# #         'total_price' : total_price,
# #         'discount': discount,
# #         # 'delevary' : delevary,
# #     }

#     return render(request, 'cart/checkout.html', context)

# All code fixed in deepseek::

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Import your models and forms
from .models import Cart, CartItem
# Assuming Coupon and ApplyCouponForm are in an app called 'coupon' or 'cart'
# Adjust import path based on where you put forms.py and models.py for Coupon
from Coupon.models import Coupon # Adjust if Coupon model is in this app's models.py
from Coupon.forms import ApplyCouponForm # Adjust if ApplyCouponForm is in this app's forms.py

# Define a fixed delivery charge
DELIVERY_CHARGE = 50.00 # Example: Tk 50.00

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

    if current_user.is_authenticated:
        # User is logged in
        cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            existing_variations_list = [list(item.variations.all()) for item in cart_items]
            ids = [item.id for item in cart_items]

            if product_variation in existing_variations_list:
                index = existing_variations_list.index(product_variation)
                item_id = ids[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if product_variation:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            if product_variation:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
    else:
        # User is not logged in
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, cart=cart)
            existing_variations_list = [list(item.variations.all()) for item in cart_items]
            ids = [item.id for item in cart_items]

            if product_variation in existing_variations_list:
                index = existing_variations_list.index(product_variation)
                item_id = ids[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if product_variation:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if product_variation:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
    return redirect('cart')

# Remove single item quantity from cart
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
    except ObjectDoesNotExist:
        pass
    return redirect('cart')

# Remove item completely from cart
def remove(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


# Cart view: Displays cart items and calculates totals
def cart(request, sub_total=0, quantity=0):
    vat = 0
    discount = 0
    final_total = 0
    cart_items = []
    coupon = None
    delivery_charge = DELIVERY_CHARGE

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            # Get or create the user's cart for coupon linking
            user_cart, created = Cart.objects.get_or_create(user=request.user)
            if user_cart.coupon and user_cart.coupon.is_valid():
                coupon = user_cart.coupon
            else:
                # Clear invalid or expired coupon from cart
                user_cart.coupon = None
                user_cart.save()
        else:
            cart_session = Cart.objects.filter(cart_id=_cart_id(request)).first()
            if cart_session:
                cart_items = CartItem.objects.filter(cart=cart_session, is_active=True)
            # For non-authenticated users, coupon is not persisted on Cart model.
            # You might use session variables if you need to track coupons for guests.

        for cart_item in cart_items:
            sub_total += cart_item.sub_total()
            quantity += cart_item.quantity

        vat = (1 * sub_total) / 100 # Example: 1% VAT

        if coupon:
            discount = (coupon.discount_percentage / 100) * sub_total

        final_total = sub_total + vat - discount + delivery_charge
        if final_total < 0:
            final_total = 0 # Prevent negative totals

    except ObjectDoesNotExist:
        pass # Cart or cart items do not exist

    # Initialize coupon form for display
    apply_coupon_form = ApplyCouponForm()

    context = {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'quantity': quantity,
        'vat': vat,
        'discount': discount,
        'delivery_charge': delivery_charge,
        'coupon': coupon, # Pass the applied coupon object
        'final_total': final_total,
        'apply_coupon_form': apply_coupon_form, # Pass the coupon form
    }
    return render(request, 'cart/cart.html', context)


# Checkout view: Displays summary and handles billing address form
@login_required(login_url='login')
def checkout(request):
    sub_total = 0
    vat = 0
    discount = 0
    final_total = 0
    cart_items = []
    coupon = None
    delivery_charge = DELIVERY_CHARGE

    try:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        if user_cart.coupon and user_cart.coupon.is_valid():
            coupon = user_cart.coupon
        else:
            user_cart.coupon = None
            user_cart.save()

        for cart_item in cart_items:
            sub_total += cart_item.sub_total()

        vat = (1 * sub_total) / 100

        if coupon:
            discount = (coupon.discount_percentage / 100) * sub_total

        final_total = sub_total + vat - discount + delivery_charge
        if final_total < 0:
            final_total = 0

    except ObjectDoesNotExist:
        messages.error(request, "Your cart is empty or an error occurred.")
        return redirect('cart')

    # The coupon application logic is now handled by the separate apply_coupon view
    # This view just prepares the context for display.
    apply_coupon_form = ApplyCouponForm()

    context = {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'vat': vat,
        'discount': discount,
        'delivery_charge': delivery_charge,
        'coupon': coupon,
        'final_total': final_total,
        'apply_coupon_form': apply_coupon_form, # Pass the form for display
    }
    return render(request, 'cart/checkout.html', context)


# Apply Coupon view: Handles the POST request for coupon application
@login_required(login_url='login')
def apply_coupon(request):
    if request.method == 'POST':
        form = ApplyCouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code)
                if coupon.is_valid():
                    # Link coupon to the user's cart
                    user_cart, created = Cart.objects.get_or_create(user=request.user)
                    # Check if the coupon is already applied and is the same
                    if user_cart.coupon == coupon:
                        messages.info(request, f'Coupon "{code}" is already applied.')
                    else:
                        user_cart.coupon = coupon
                        user_cart.save()
                        messages.success(request, f'Coupon "{code}" applied successfully!')
                else:
                    messages.error(request, 'This coupon is not valid, expired, or fully used.')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code. Please check the code and try again.')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
        else:
            messages.error(request, 'Please enter a valid coupon code.')
    return redirect('checkout') # Redirect back to checkout to refresh calculations and display messages