from django.shortcuts import render, redirect, get_object_or_404
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
import datetime
from django.http import HttpResponse, JsonResponse
from carts.models import Coupon, DeliveryMethod

from django.utils import timezone
import datetime
from store.models import Product, Variation

import stripe
import json
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    #tax ar jnno kicu code likhbo:
    vat = 0
    total_price = 0
    discount_amount = 0
    delivery_charge = 0
   
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    vat = (1 * total)/100
    # total_price = total + vat # akn a je vat dilam aita ke amra niche ar ai app a models.py a tax hisabe dorci
    coupon_id = request.session.get('coupon_id')
    coupon = None
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.is_valid(order.total):
                discount_amount = coupon.get_discount_amount(order.total)
        except Coupon.DoesNotExist:
            discount_amount = 0
    delivery_method_id = request.POST.get('delivery_method')
    delivery_method = None
    if delivery_method_id:
        try:
            delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)
            delivery_charge = delivery_method.price
        except DeliveryMethod.DoesNotExist:
            delivery_charge = 0
    total_price = total + vat  + delivery_charge - discount_amount

    if request.method =='POST':

        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user= current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email =form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = total_price.cleaned_data['order_total']
            data.order_total = total_price
            data.tax = vat
            data.discount = discount_amount
            data.delivery_charge = delivery_charge

            if coupon:
                data.coupon = coupon
            if delivery_method:
                data.delivery_method = delivery_method
            data.ip = request.META.get('REMOTE_ADDR')
            
            data.save()

            #akn a date ke venge likhbo
            year = int(datetime.date.today().strftime('%Y'))
            date_time = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            d = datetime.datetime(year,month,date_time)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)

            data.order_number = order_number
            data.save()
            if coupon:
                coupon.used_count += 1
                coupon.save()
            order = Order.objects.get(user=current_user, is_ordered=False,order_number=order_number)
            context = { #payment method kete dileo ai line takbe kintu
                'order' : order, #payment method kete dileo ai line takbe kintu
                'cart_items' : cart_items, #payment method kete dileo ai line takbe kintu
                'total' : total, #payment method kete dileo ai line takbe kintu
                'vat' : vat, #payment method kete dileo ai line takbe kintu
                'discount_amount': discount_amount, # নতুন যোগ করুন
                'delivery_charge': delivery_charge, # নতুন যোগ করুন
                'total_price' : total_price, #payment method kete dileo ai line takbe kintu
                'coupon_code': coupon.code if coupon else None, # নতুন যোগ করুন
            }
            if 'coupon_id' in request.session:
                del request.session['coupon_id']
            if 'coupon_code' in request.session:
                del request.session['coupon_code']
            #end payment method
            
            
            return render(request, 'payment/payment.html', context)
        
        else:
            return redirect('checkout')
