from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from order.views import send_order_confirmation_email
from .models import Order, OrderProduct, Payment
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem,Coupon, DeliveryMethod 
from store.models import Product, Variation
from django.core.mail import EmailMessage
from .forms import OrderForm, PaymentForm
from accounts.models import Account
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from django.conf import settings
from .models import Payment
from datetime import datetime
import datetime
import random
import string
import json

def order_complete(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    
    try:
        order = Order.objects.get(order_number=order_id, is_ordered=True)
        payment = Payment.objects.get(payment_id=payment_id)
        order_products = OrderProduct.objects.filter(order=order)
        
        context = {
            'order': order,
            'payment': payment,
            'order_products': order_products,
        }
        return render(request, 'order/order_complete.html', context)
        
    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('home')


@login_required(login_url='login')
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    
    if cart_items.count() <= 0:
        messages.warning(request, "Your cart is empty!")
        return redirect('store')
    #tax ar jnno kicu code likhbo:
    vat = 0
    total_price = 0
    # discount_amount = 0
    # delivery_charge = 0
   
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    # vat = (1 * total)/100
    vat = total * 0.01

     # Coupon calculation
    coupon = None
    discount_amount = 0
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.is_valid(total):
                discount_amount = coupon.get_discount_amount(total)
        except Coupon.DoesNotExist:

            discount_amount = 0

    # Delivery charge calculation
     # Delivery charge calculation
    delivery_method = None
    delivery_charge = 0
    # delivery_method_id = request.POST.get('delivery_method')
    delivery_method_id = request.session.get('delivery_method_id')

    if delivery_method_id:
        try:
            delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)
            delivery_charge = delivery_method.price
        except DeliveryMethod.DoesNotExist:
            delivery_charge = 0
    total_price = total + vat + delivery_charge - discount_amount
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = current_user
                    order.order_total = total
                    order.tax = vat
                    order.discount = discount_amount
                    order.delivery_charge = delivery_charge
                    order.grand_total = total_price
                    order.ip = request.META.get('REMOTE_ADDR')

                    if coupon:
                        order.coupon = coupon
                    if delivery_method:
                        order.delivery_method = delivery_method
                    order.save()

                    # Generate order number
                    year = datetime.now().year
                    month = datetime.now().month
                    day = datetime.now().day
                    order_number = f"{year}{month:02d}{day:02d}{order.id}"
                    order.order_number = order_number
                    order.save()

                    # Update coupon usage
                    if coupon:
                        coupon.used_count += 1
                        coupon.save()
                    request.session['order_id'] = order.id

                    context = {
                        'order': order,
                        'cart_items': cart_items,
                        'total': total,
                        'vat': vat,
                        'discount_amount': discount_amount,
                        'delivery_charge': delivery_charge,
                        'total_price': total_price,
                        'coupon_code': coupon.code if coupon else None,
                    }
                    if 'coupon_id' in request.session:
                        del request.session['coupon_id']
                    if 'coupon_code' in request.session:
                        del request.session['coupon_code']

                    messages.success(request, "Order placed successfully!")
                    return render(request, 'payment/payment.html', context)
            except Exception as e:
                messages.error(request, f"Error placing order: {str(e)}")
                return redirect('checkout')
        else:
            messages.error(request, "Invalid order form. Please check your details.")
            return redirect('checkout')
    
    return redirect('checkout')



@login_required(login_url='login')
def payments(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order_id = request.session.get('order_id')
                    if not order_id:
                        messages.error(request, "No order found. Please place order first.")
                        return redirect('place_order')
                    order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
                    payment_method = form.cleaned_data['payment_method']
                    payment = Payment(
                        user=request.user,
                        payment_method=payment_method,
                        amount_paid=order.grand_total,
                        status='completed' if payment_method != 'cod' else 'pending'
                    )
                    if payment_method in ['bkash', 'nagad', 'rocket', 'upay']:
                        payment.mobile_number = form.cleaned_data['mobile_number']
                        payment.transaction_id = form.cleaned_data['transaction_id']

                    elif payment_method in ['card', 'emi']:
                        payment.card_number = form.cleaned_data['card_number'][-4:]
                        payment.card_holder_name = form.cleaned_data['card_holder_name']

                        if payment_method == 'emi':
                            payment.emi_month = form.cleaned_data['emi_month']
                    payment.save()

                    order.payment = payment
                    order.is_ordered = True
                    order.status = 'Accepted' if payment_method != 'cod' else 'New'
                    order.save()

                    cart_items = CartItem.objects.filter(user=request.user)
                    for cart_item in cart_items:
                        order_product = OrderProduct()
                        order_product.order = order
                        order_product.payment = payment
                        order_product.user = request.user
                        order_product.product = cart_item.product
                        order_product.quantity = cart_item.quantity
                        order_product.product_price = cart_item.product.price
                        order_product.ordered = True
                        order_product.save()

                        # Add variations
                        for variation in cart_item.variations.all():
                            order_product.variations.add(variation)
                        
                        product = cart_item.product
                        product.stock -= cart_item.quantity
                        product.save()
                    cart_items.delete()

                    # Send order confirmation email
                    send_order_confirmation_email(order, payment, request.user)
                    context = {
                        'order': order,
                        'payment': payment,
                        'order_products': OrderProduct.objects.filter(order=order),
                    }
                    if 'order_id' in request.session:
                        del request.session['order_id']
                    
                    messages.success(request, "Payment completed successfully!")
                    return render(request, 'payment/order_complete.html', context)
            except Order.DoesNotExist:
                messages.error(request, "Order does not exist.")
                return redirect('place_order')
            
            except Exception as e:
                messages.error(request, f"Error payment failed: {str(e)}")
                return redirect('checkout')
            
    else:
        # GET request - show payment form
        order_id = request.session.get('order_id')
        if not order_id:
            messages.error(request, "No order found. Please place order first.")
            return redirect('place_order')
        order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
        form = PaymentForm()
        
        context = {
            'order': order,
            'form': form,
        }
        return render(request, 'payment/payment.html', context)