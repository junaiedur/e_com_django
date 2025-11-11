from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse 
from django.db import transaction
from django.utils import timezone
from order.models import Order, Payment, OrderProduct 
from carts.models import CartItem 
from order.views import send_order_confirmation_email
from .service import BkashPaymentService
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# bKash payment by deepseek:


@login_required
def initiate_bkash_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, is_ordered=False)
# Generate unique merchant invoice number
    merchant_invoice = f"INV{order.order_number}{timezone.now().strftime('%H%M%S')}"
    bkash_service = BkashPaymentService()
    result = bkash_service.create_payment(
        amount=order.grand_total,
        order_id=order.id,
        merchant_invoice=merchant_invoice
    )
    if result['success']:
        # Save payment info temporarily
        request.session['bkash_payment_id'] = result['payment_id']
        request.session['current_order_id'] = order.id
        request.session['merchant_invoice'] = merchant_invoice
        return JsonResponse({
            'success': True,
            'bkash_url': result['bkash_url'],
            'payment_id': result['payment_id']
        })
    else:
        return JsonResponse ({
            'success': False,
            'error': result['error']
        })


@csrf_exempt
def bkash_callback(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('paymentID')
            status = request.POST.get('status')
            if status == 'success':
                bkash_service = BkashPaymentService()
                execute_result = bkash_service.execute_payment(payment_id)
                
                if execute_result.get('statusCode') == '0000':
                     # Payment successful
                    return handle_successful_payment(request, execute_result)
                else:
                    return handle_successful_payment(request, execute_result)
            else:
                return handle_successful_payment(request, {'status': 'failed'})
        
        except Exception as e:
            return handle_successful_payment(request, {'error': str(e)})
        
    return redirect('payment_failed')

def handle_successful_payment(request, payment_data):
    try:
        order_id = request.session.get('current_order_id')
        order = Order.objects.get(id=order_id)
        payment = Payment(
            user=request.user,
            payment_method='bkash',
            amount_paid=order.grand_total,
            status='completed',
            bkash_payment_id=payment_data.get('paymentID'),
            bkash_transaction_id=payment_data.get('trxID'),
            bkash_merchant_invoice=request.session.get('merchant_invoice'),
            bkash_create_time=timezone.now()
        )
        payment.save()

        # Update order
        order.payment = payment
        order.is_ordered = True
        order.status = 'Accepted'
        order.save()

         # Clear session
        if 'bkash_payment_id' in request.session:
            del request.session['bkash_payment_id']
        if 'current_order_id' in request.session:
            del request.session['current_order_id']
        if 'merchant_invoice' in request.session:
            del request.session['merchant_invoice']

        # Redirect to success page
        #return redirect('invoice', order_number=order.order_number)
        return redirect(reverse('payment:invoice', kwargs={'order_number': order.order_number}))


    except Exception as e:
        return redirect('payment_failed')
    

# def handle_failled_payment(request, error_data):
#     if 'bkash_payment_id' in request.session:
#         del request.session['bkash_payment_id']
#     if 'current_order_id' in request.session:
#         del request.session['current_order_id']
    
#     return redirect('payment_failed')
def handle_failed_payment(request, error_data):
    # optional: log error_data
    request.session.pop('bkash_payment_id', None)
    request.session.pop('current_order_id', None)
    request.session.pop('merchant_invoice', None)
    return redirect('payment_failed')

@login_required
def payment_success(request):
    """Payment success page"""
    return render(request, 'payment/payment_success.html')

@login_required
def payment_failed(request):
    """Payment failed page"""
    return render(request, 'payment/payment_failed.html')


    # if status == 'cancel' or status == 'failure':
    #     try:
    #         payment = Payment.objects.get(payment_id=payment_id)
    #         payment.status = 'failed'
    #         payment.save()
    #     except Payment.DoesNotExist:
    #         pass

    #     messages.error(request, "bKash payment was cancelled or failed.")
    #     return redirect('payments')
    
    # if status == 'success' and payment_id:
    #     execution_response = execute_payment(payment_id) 

    #     if execution_response.get("status") == "success":
    #         payment_data = execution_response["data"]
    #         trx_id = payment_data.get('trxID')
    #         order_id = payment_data.get('merchantInvoiceNumber')
    #         try:
    #             with transaction.atomic():
    #                 order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
    #                 payment = Payment.objects.get(payment_id=payment_id)

    #                 payment.transaction_id = trx_id
    #                 payment.status = 'completed'
    #                 payment.save()

    #                 order.payment = payment
    #                 order.is_ordered = True
    #                 order.status = 'Accepted'
    #                 order.save()

    #                 cart_items = CartItem.objects.filter(user=request.user)
    #                 for item in cart_items:
    #                     order_product = OrderProduct(
    #                         order=order,
    #                         payment=payment,
    #                         user=request.user,
    #                         product=item.product,
    #                         quantity=item.quantity,
    #                         product_price=item.product.price,
    #                         ordered=True,
    #                     )
    #                     order_product.save()
    #                     for variation in item.variations.all():
    #                         order_product.variations.add(variation)
                        
    #                     item.product.stock -= item.quantity
    #                     item.product.save()
    #                 cart_items.delete()

    #                 if 'order_id' in request.session:
    #                     del request.session['order_id']
                    
    #                 send_order_confirmation_email(order, payment, request.user)
                
    #             success_url = f"{reverse('order_complete')}?order_id={order.order_number}&payment_id={payment.id}"
    #             return redirect(success_url)
            
    #         except Order.DoesNotExist:
    #             messages.error(request, "Order not found.")
    #             return redirect('store')
    #         except Payment.DoesNotExist:
    #             messages.error(request, "Payment not found.")
    #             return redirect('store')
    #         except Exception as e:
    #             messages.error(request, f"An error occurred: {str(e)}")
    #             return redirect('store')

    #     else:
    #         messages.error(request, "bKash payment verification failed.")
    #         return redirect('payments')


    # messages.error(request, "Invalid bKash callback.")
    # return redirect('payments')