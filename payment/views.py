from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse 
from django.db import transaction

from order.models import Order, Payment, OrderProduct # আপনার order app থেকে ইম্পোর্ট করুন
from carts.models import CartItem # আপনার carts app থেকে ইম্পোর্ট করুন
from order.views import send_order_confirmation_email # আপনার order view থেকে ইমেইল ফাংশন

from .bkash_service import create_payment, execute_payment
import json
from django.contrib import messages

@csrf_exempt
def initiate_bkash_payment(request):
    if request.method == 'POST':
        order_id = request.session.get('order_id')
        if not order_id:
            return JsonResponse({"status": "error", "message": "Order ID not found in session."})
        try:
            order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Order not found."})
        # bKash এ পেমেন্ট রিকোয়েস্ট পাঠানোর জন্য কলব্যাক URL
        # এটি অবশ্যই একটি ফুল ডোমেইন URL হতে হবে
        callback_url = request.build_absolute_uri(reverse('bkash_payment_callback'))

        # bKash সার্ভিস কল করুন
        payment_data = create_payment(order.grand_total, order.id, callback_url)

        if payment_data.get("status") == "success":
            # bKash পেমেন্ট অবজেক্ট তৈরি করুন (কিন্তু স্ট্যাটাস pending থাকবে)
            Payment.objects.create(
                user=request.user,
                payment_id=payment_data['paymentID'], # bKash paymentID
                payment_method='bkash',
                amount_paid=order.grand_total,
                status='pending'
            )
            return JsonResponse(payment_data)
        else:
            return JsonResponse(payment_data)
    return JsonResponse({"status": "error", "message": "Invalid request method."})

@csrf_exempt
def bkash_payment_callback(request):
    payment_id = request.GET.get('paymentID')
    status = request.GET.get('status')
    if status == 'cancel' or status == 'failure':
        try:
            payment = Payment.objects.get(payment_id=payment_id)
            payment.status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass

        messages.error(request, "bKash payment was cancelled or failed.")
        return redirect('payments')
    
    if status == 'success' and payment_id:
        execution_response = execute_payment(payment_id) 

        if execution_response.get("status") == "success":
            payment_data = execution_response["data"]
            trx_id = payment_data.get('trxID')
            order_id = payment_data.get('merchantInvoiceNumber') # আমরা এটা order.id হিসেবে সেট করেছিলাম
            try:
                with transaction.atomic():
                    # অর্ডার এবং পেমেন্ট আপডেট করুন
                    order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
                    payment = Payment.objects.get(payment_id=payment_id)

                    payment.transaction_id = trx_id
                    payment.status = 'completed'
                    payment.save()

                    order.payment = payment
                    order.is_ordered = True
                    order.status = 'Accepted'
                    order.save()

                    # আপনার order_views.py এর payments ফাংশন থেকে লজিক কপি করুন
                    # Cart items গুলোকে OrderProduct এ মুভ করুন
                    cart_items = CartItem.objects.filter(user=request.user)
                    for item in cart_items:
                        order_product = OrderProduct(
                            order=order,
                            payment=payment,
                            user=request.user,
                            product=item.product,
                            quantity=item.quantity,
                            product_price=item.product.price,
                            ordered=True,
                        )
                        order_product.save()
                        for variation in item.variations.all():
                            order_product.variations.add(variation)
                        
                        item.product.stock -= item.quantity
                        item.product.save()
                    cart_items.delete()

                    if 'order_id' in request.session:
                        del request.session['order_id']
                    
                    send_order_confirmation_email(order, payment, request.user)
                
                # সফলভাবে পেমেন্ট হলে ইউজারকে order_complete পে
                success_url = f"{reverse('order_complete')}?order_id={order.order_number}&payment_id={payment.id}"
                return redirect(success_url)
            
            except Order.DoesNotExist:
                messages.error(request, "Order not found.")
                return redirect('store')
            except Payment.DoesNotExist:
                messages.error(request, "Payment not found.")
                return redirect('store')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('store')

        else:
            messages.error(request, "bKash payment verification failed.")
            return redirect('payments')


    messages.error(request, "Invalid bKash callback.")
    return redirect('payments')