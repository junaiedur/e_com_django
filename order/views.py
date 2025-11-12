# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Order, OrderProduct, Payment
# from django.views.decorators.csrf import csrf_exempt
# from django.template.loader import render_to_string
# from django.http import HttpResponse, JsonResponse
# from carts.models import CartItem, Coupon, DeliveryMethod 
# from store.models import Product, Variation
# from django.core.mail import EmailMessage
# from .forms import OrderForm, PaymentForm
# from accounts.models import Account
# from django.contrib import messages
# from django.utils import timezone
# from django.db import transaction
# from decimal import Decimal
# from django.conf import settings
# from .models import Payment, Order, OrderProduct
# from datetime import datetime
# import datetime

# #3
# def order_complete(request):
#     order_id = request.GET.get('order_id')
#     payment_id = request.GET.get('payment_id')
    
#     try:
#         order = Order.objects.get(order_number=order_id, is_ordered=True)
#         payment = Payment.objects.get(payment_id=payment_id)
#         order_products = OrderProduct.objects.filter(order=order)
        
#         context = {
#             'order': order,
#             'payment': payment,
#             'order_products': order_products,
#         }
#         return render(request, 'order/order_complete.html', context)
        
#     except (Order.DoesNotExist, Payment.DoesNotExist):
#         return redirect('home')

# #1
# @login_required(login_url='login')
# def place_order(request, total=0, quantity=0):
#     current_user = request.user
#     cart_items = CartItem.objects.filter(user=current_user)
    
#     if cart_items.count() <= 0:
#         messages.warning(request, "Your cart is empty!")
#         return redirect('store')
#     #tax ar jnno kicu code likhbo:
#     vat = 0
#     total_price = 0
#     quantity = 0
#     # discount_amount = 0
#     # delivery_charge = 0
   
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
    
#     # vat = (1 * total)/100
#     vat = total * Decimal('0.01') # '0.01' কে Decimal এ রূপান্তর করুন

#      # Coupon calculation
#     coupon = None
#     discount_amount = 0
#     coupon_id = request.session.get('coupon_id')
#     if coupon_id:
#         try:
#             coupon = Coupon.objects.get(id=coupon_id)
#             if coupon.is_valid(total):
#                 discount_amount = coupon.get_discount_amount(total)
#         except Coupon.DoesNotExist:

#             discount_amount = 0

#     # Delivery charge calculation
#      # Delivery charge calculation
#     delivery_method = None
#     delivery_charge = 0
#     # delivery_method_id = request.POST.get('delivery_method')
#     delivery_method_id = request.session.get('delivery_method_id')

#     if delivery_method_id:
#         try:
#             delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)
#             delivery_charge = delivery_method.price
#         except DeliveryMethod.DoesNotExist:
#             delivery_charge = 0

#     total_price = total + vat + delivery_charge - discount_amount
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     order = form.save(commit=False)
#                     order.user = current_user
#                     order.order_total = total
#                     order.tax = vat
#                     order.discount = discount_amount
#                     order.delivery_charge = delivery_charge
#                     order.grand_total = total_price
#                     order.ip = request.META.get('REMOTE_ADDR')

#                     if coupon:
#                         order.coupon = coupon
#                     if delivery_method:
#                         order.delivery_method = delivery_method
#                     order.save()

#                     # Generate order number
#                     year = datetime.now().year
#                     month = datetime.now().month
#                     day = datetime.now().day
#                     order_number = f"{year}{month:02d}{day:02d}{order.id}"
#                     order.order_number = order_number
#                     order.save()

#                     # Update coupon usage
#                     if coupon:
#                         coupon.used_count += 1
#                         coupon.save()
#                     request.session['order_id'] = order.id
#                     request.session['order_number'] = order_number
                    
#                     context = {
#                         'order': order,
#                         'form': form,
#                         'cart_items': cart_items,
#                         'total': total,
#                         'vat': vat,
#                         'discount_amount': discount_amount,
#                         'delivery_charge': delivery_charge,
#                         'total_price': total_price,
#                         'coupon_code': coupon.code if coupon else None,
#                     }
#                     #cleaning method process:
#                     if 'coupon_id' in request.session:
#                         del request.session['coupon_id']
#                     if 'coupon_code' in request.session:
#                         del request.session['coupon_code']

#                     messages.success(request, "Order placed successfully!")
#                     return render(request, 'payment/payment.html', context)
            
#             except Exception as e:
#                 messages.error(request, f"Error placing order: {str(e)}")
#                 return redirect('checkout')
#         else:
#             messages.error(request, "Invalid order form. Please check your details.")
#             return redirect('checkout')
        
#     #POST menthod kam nah korle ai rediret kam kobro
#     return redirect('checkout')











#     # # total_price = total + vat # akn a je vat dilam aita ke amra niche ar ai app a models.py a tax hisabe dorci
#     # coupon_id = request.session.get('coupon_id')
#     # coupon = None
#     # if coupon_id:
#     #     try:
#     #         coupon = Coupon.objects.get(id=coupon_id)
#     #         discount_amount = coupon.get_discount_amount(total)
#     #         # if coupon.is_valid(order.total):
#     #         #     discount_amount = coupon.get_discount_amount(order.total)
#     #     except Coupon.DoesNotExist:
#     #         discount_amount = 0
#     # delivery_method_id = request.POST.get('delivery_method')
#     # delivery_method = None
#     # if delivery_method_id:
#     #     try:
#     #         delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)
#     #         delivery_charge = delivery_method.price
#     #     except DeliveryMethod.DoesNotExist:
#     #         delivery_charge = 0
#     # total_price = total + vat  + delivery_charge - discount_amount

#     # if request.method =='POST':

#     #     form = OrderForm(request.POST)
#     #     if form.is_valid():
#     #         data = Order()
#     #         data.user= current_user
#     #         data.first_name = form.cleaned_data['first_name']
#     #         data.last_name = form.cleaned_data['last_name']
#     #         data.phone = form.cleaned_data['phone']
#     #         data.email =form.cleaned_data['email']
#     #         data.address_line_1 = form.cleaned_data['address_line_1']
#     #         data.address_line_2 = form.cleaned_data['address_line_2']
#     #         data.country = form.cleaned_data['country']
#     #         data.state = form.cleaned_data['state']
#     #         data.city = form.cleaned_data['city']
#     #         data.order_note = form.cleaned_data['order_note']
#     #         data.order_total = total_price.cleaned_data['order_total']
#     #         data.order_total = total_price
#     #         data.tax = vat
#     #         data.discount = discount_amount
#     #         data.delivery_charge = delivery_charge

#     #         if coupon:
#     #             data.coupon = coupon
#     #         if delivery_method:
#     #             data.delivery_method = delivery_method
#     #         data.ip = request.META.get('REMOTE_ADDR')
            
#     #         data.save()

#     #         #akn a date ke venge likhbo
#     #         year = int(datetime.date.today().strftime('%Y'))
#     #         date_time = int(datetime.date.today().strftime('%d'))
#     #         month = int(datetime.date.today().strftime('%m'))
#     #         d = datetime.datetime(year,month,date_time)
#     #         current_date = d.strftime("%Y%m%d")
#     #         order_number = current_date + str(data.id)
#     #         data.order_number = order_number
#     #         data.save()

#     #         request.session['order_id'] = data.id


#     #         if coupon:
#     #             coupon.used_count += 1
#     #             coupon.save()
#     #         order = Order.objects.get(user=current_user, is_ordered=False,order_number=order_number)
#     #         context = { #payment method kete dileo ai line takbe kintu
#     #             'order' : order, #payment method kete dileo ai line takbe kintu
#     #             'cart_items' : cart_items, #payment method kete dileo ai line takbe kintu
#     #             'total' : total, #payment method kete dileo ai line takbe kintu
#     #             'vat' : vat, #payment method kete dileo ai line takbe kintu
#     #             'discount_amount': discount_amount, # নতুন যোগ করুন
#     #             'delivery_charge': delivery_charge, # নতুন যোগ করুন
#     #             'total_price' : total_price, #payment method kete dileo ai line takbe kintu
#     #             'coupon_code': coupon.code if coupon else None, # নতুন যোগ করুন
#     #         }
#     #         if 'coupon_id' in request.session:
#     #             del request.session['coupon_id']
#     #         if 'coupon_code' in request.session:
#     #             del request.session['coupon_code']
#     #         #end payment method
            
            
#     #         return render(request, 'payment/payment.html', context)
        
#     #     else:
#             # return redirect('checkout')


# #2
# @login_required(login_url='login')
# def payments(request):
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     order_id = request.session.get('order_id')
#                     if not order_id:
#                         messages.error(request, "No order found. Please place order first.")
#                         return redirect('place_order')
#                     order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
#                     payment_method = form.cleaned_data['payment_method']
                    
#                     #  payment er jnno:
#                     payment = Payment(
#                         user=request.user,
#                         payment_method=payment_method,
#                         amount_paid=order.grand_total,
#                         status='completed' if payment_method != 'cod' else 'pending'
#                     )
#                     # Set additional payment details based on method
#                     if payment_method in ['bkash', 'nagad', 'rocket', 'upay']:
#                         payment.mobile_number = form.cleaned_data['mobile_number']
#                         payment.transaction_id = form.cleaned_data['transaction_id']
#                     elif payment_method in ['card', 'emi']:
#                         payment.card_number = form.cleaned_data['card_number'][-4:]
#                         payment.card_holder_name = form.cleaned_data['card_holder_name']
#                         if payment_method == 'emi':
#                             payment.emi_month = form.cleaned_data['emi_month']
#                     payment.save()
#                     # Update order
#                     order.payment = payment
#                     order.is_ordered = True
#                     order.status = 'Accepted' if payment_method != 'cod' else 'New'
#                     order.save()
#                     # Create order products
#                     cart_items = CartItem.objects.filter(user=request.user)
#                     for cart_item in cart_items:
#                         order_product = OrderProduct()
#                         order_product.order = order
#                         order_product.payment = payment
#                         order_product.user = request.user
#                         order_product.product = cart_item.product
#                         order_product.quantity = cart_item.quantity
#                         order_product.product_price = cart_item.product.price
#                         order_product.ordered = True
#                         order_product.save()
#                          # Add variations
#                         for variation in cart_item.variations.all():
#                             order_product.variations.add(variation)
#                         # Reduce product stock
#                         product = cart_item.product
#                         product.stock -= cart_item.quantity
#                         product.save()
#                     cart_item.delete()

#                     # Send confirmation email
#                     send_order_confirmation_email(order, payment, request.user)

#                     # Prepare success URL
#                     success_url = f"/order/order_complete/?order_id={order.order_number}&payment_id={payment.payment_id}"

#             except Order.DoesNotExist:
#                 messages.error(request, "Order does not exist.")
#                 return redirect('place_order')
#             except Exception as e:
#                 messages.error(request, f"Error in payment: {str(e)}")
#                 return redirect('checkout')

#     order_id = request.session.get('order_id')
#     if not order_id:
#         messages.error(request, "No order found. Please place order first.")
#         return redirect('place_order')
#     try:
#         order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
#         form = PaymentForm()
        
#         context = {
#             'order': order,
#             'form': form,
#         }
#         return render(request, 'payment/payment.html', context)
    
#     except Order.DoesNotExist:
#         messages.error(request, "Order not found.")
#         return redirect('place_order')


    
#     # else:
#     #     order_id = request.session.get('order_id')
#     #     if not order_id:
#     #         messages.error(request, "No order found. Please place order first.")
#     #         return redirect('place_order')
#     #     order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
#     #     form = PaymentForm()
            
#     #     context = {
#     #         'order': order,
#     #         'form': form,
#     #     }
#     #     return render(request, 'payment/payment.html', context)

#     #     order_id = request.session.get('order_id')
#     #     order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
#     #         # if not order_id:
#     #         #     messages.error(request, "No order found. Please place order first.")
#     #         #     return redirect('place_order')
#     #         # order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
#     #         # form = PaymentForm()
#     #     context = {
#     #         'order': order,
#     #         'form': form,
#     #     }
#     #     messages.error(request, "Please correct the errors below.")
#     #     return render(request, 'payment/payment.html', context)
        

#     # else:
#     #     # GET request - show payment form
#     #     order_id = request.session.get('order_id')
#     #     if not order_id:
#     #         messages.error(request, "No order found. Please place order first.")
#     #         return redirect('place_order')
#     #     order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
#     #     form = PaymentForm()
        
#     #     context = {
#     #         'order': order,
#     #         'form': form,
#     #     }
#     #     return render(request, 'payment/payment.html', context)
#     # if form.is_valid():
#     #     try:
#     #         with transaction.atomic():
#     #             order_id = request.session.get('order_id')
#     #             if not order_id:
#     #                 messages.error(request, "No order found. Please place order first.")
#     #                 return redirect('place_order')
                
#     #             order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)

#     #             payment_method = form.cleaned_data['payment_method']

#     #             payment = Payment(
#     #                 user = request.user,
#     #                 payment_method=form.cleaned_data['payment_method'],
#     #                 amount_paid=order.grand_total,
#     #                 status='completed' if form.cleaned_data['payment_method'] != 'cod' else 'pending'
#     #             )
#     #             # payment_method = form.cleaned_data['payment_method']
                    
#     #             if payment_method in ['bkash', 'nagad', 'rocket', 'upay']:
#     #                 payment.mobile_number = form.cleaned_data['mobile_number']
#     #                 payment.transaction_id = form.cleaned_data['transaction_id']
                
#     #             elif payment_method in ['card', 'emi']:
#     #                 payment.card_number = form.cleaned_data['card_number'][-4:]
#     #                 payment.card_holder_name = form.cleaned_data['card_holder_name']
                    
#     #                 if payment_method == 'emi':
#     #                     payment.emi_month = form.cleaned_data['emi_month']
#     #                     payment.emi_interest = 12.0
            
#     #             payment.save()

#     #             # Update order with payment
#     #             order.payment = payment
#     #             order.is_ordered = True
#     #             order.status = 'Accepted' if payment_method != 'cod' else 'New'
#     #             order.save()

#     #             # Move cart items to order products
#     #             cart_items = CartItem.objects.filter(user=request.user)
#     #             for cart_item in cart_items:
#     #                 order_product = OrderProduct()
#     #                 order_product.order = order
#     #                 order_product.payment = payment
#     #                 order_product.user = request.user
#     #                 order_product.product = cart_item.product
#     #                 order_product.quantity = cart_item.quantity
#     #                 order_product.product_price = cart_item.product.price
#     #                 order_product.ordered = True
#     #                 order_product.save()

#     #                 # Add variations
#     #                 for variation in cart_item.variations.all():
#     #                     order_product.variations.add(variation)
#     #                 # Reduce product stock
#     #                 product = cart_item.product
#     #                 product.stock -= cart_item.quantity
#     #                 product.save()
#     #             cart_items.delete()

#     #             # Send order confirmation email
#     #             send_order_confirmation_email(order, payment, request.user)

#     #             # send_order_email(order, payment, request.user)
#     #             context = {
#     #                 'order': order,
#     #                     'payment': payment,
#     #                     'order_products': OrderProduct.objects.filter(order=order),
#     #             }

#     #             if 'order_id' in request.session:
#     #                 del request.session['order_id']
                
#     #             messages.success(request, "Payment completed successfully!")
#     #             return render(request, 'payment/order_complete.html', context)
        
#     #     except Order.DoesNotExist:
#     #         messages.error(request, "Order does not exist.")
#     #         return redirect('place_order')
        
#     #     except Exception as e:
#     #         messages.error(request, f"Error payment failed: {str(e)}")
#     #         return redirect('checkout')
            
#     # else:
#     #     order_id = request.session.get('order_id')
#     #     order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
        
#     #     context = {
#     #             'order': order,
#     #             'form': form,
#     #             'form_errors': form.errors
#     #     }
        
#     #     messages.error(request, "Please correct the payment information.")
#     #     return render(request, 'payment/payment.html', context)
    
#     # return redirect('place_order')




# # ####
# #     order_id = request.session.get('order_id')
# #     order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
# #     # Generate payment ID
# #     payment_id = generate_payment_id()

# #     # Create payment record
# #     payment = Payment(
# #         user=request.user,
# #         payment_id=payment_id,
# #         payment_method=form.cleaned_data['payment_method'],
# #         amount_paid=order.order_total,
# #         status='pending'
# #     )

# #     # Save additional payment details based on method
# #     payment_method = form.cleaned_data['payment_method']
# #     if payment_method in ['bkash', 'nagad', 'rocket', 'upay']:
# #         payment.mobile_number = form.cleaned_data['mobile_number']
# #         payment.transaction_id = form.cleaned_data['transaction_id']
# #         payment.status = 'completed'  # Assuming mobile payments are instant
        
# #     elif payment_method == 'card':
# #         payment.card_number = form.cleaned_data['card_number'][-4:] # Store only last 4 digits
# #         payment.card_holder_name = form.cleaned_data['card_holder_name']
# #         payment.expiry_date = form.cleaned_data['expiry_date']
# #         payment.status = 'completed'

# #         #emi payment system:
# #     elif payment_method == 'emi':
# #         payment.card_number = form.cleaned_data['card_number'][-4:] # Store only last 4 digits
# #         payment.emi_month = form.cleaned_data['emi_month']
# #         payment.status = 'completed'

# #         #cod payment system:
# #     elif payment_method == 'cod':
# #         payment.status = 'pending'  # COD payments are pending until delivery
        
# #     payment.save()

# #         # Update order with payment
# #     order.payment = payment
# #     order.is_ordered = True
# #     order.status = 'Accepted' if payment_method != 'cod' else 'New'
# #     order.save()
        
# #      #cart items to order products
# #     cart_items = CartItem.objects.filter(user=request.user)
# #     for item in cart_items:
# #         order_product = OrderProduct()
# #         order_product.order = order
# #         order_product.payment = payment
# #         order_product.user = request.user
# #         order_product.product = item.product
# #         order_product.quantity = item.quantity
# #         order_product.product_price = item.product.price
# #         order_product.ordered = True
# #         order_product.save()

# #             # Variations:
# #         for variation in item.variations.all():
# #             order_product.variations.add(variation)
            
# #         #product quantity reduce korbo:
# #         product = Product.objects.get(id=item.product.id)
# #         product.stock -= item.quantity
# #         product.save()
# #     cart_items.delete()

# #     # Send order confirmation email
# #     send_order_email(order, payment, request.user)

# #     context = {
# #             'order': order,
# #             'payment': payment,
# #             'order_products': OrderProduct.objects.filter(order=order)
# #     }
# #     return render(request, 'payment/order_complete.html', context)
    
# #     # else:
# #     order_id = request.session.get('order_id')
# #     order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)

# #     context = {
# #         'order': order,
# #         'form_errors': form.errors
# #     }
# #     return render(request, 'payment/payment.html', context)
# # #########


# #     return redirect('checkout')

# #4
# def send_order_confirmation_email(order, payment, user):
#     try:
#         mail_subject = f'Order Confirmation - {order.order_number}'
#         message = render_to_string('emails/order_confirmation.html', {
#             'user': user,
#             'order': order,
#             'payment': payment,
#             # 'order_products': OrderProduct.objects.filter(order=order),
#         })
#         email = EmailMessage(
#             mail_subject,
#             message,
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email]
#         )

#         email.content_subtype = "html"
#         email.send()

#         #  # Also send to admin (optional)
#         # admin_message = render_to_string('emails/order_notification_admin.html', {
#         #     'order': order,
#         #     'payment': payment,
#         # })
#         # admin_email = EmailMessage(
#         #     f'New Order Received - {order.order_number}',
#         #     admin_message,
#         #     settings.DEFAULT_FROM_EMAIL,
#         #     [settings.ADMIN_EMAIL]  # Add admin email in settings
#         # )
#         # admin_email.content_subtype = "html"
#         # admin_email.send()
        
#     except Exception as e:
#         # Log email error but don't break the order process
#         print(f"Email sending failed: {str(e)}")


# @login_required(login_url='login')
# def order_history(request):
#     orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
#     context = {
#         'orders': orders,
#     }
#     return render(request, 'payment/order_history.html', context)

# @login_required(login_url='login')
# def order_detail(request, order_number):
#     order = get_object_or_404(Order, order_number=order_number, user=request.user)
#     order_products = OrderProduct.objects.filter(order=order)
    
#     context = {
#         'order': order,
#         'order_products': order_products,
#     }
#     return render(request, 'payment/order_detail.html', context)





# # Generate a unique payment ID
# # def generate_payment_id():
# #     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
# #     random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
# #     return f'PAY{timestamp}{random_str}'

# # def send_order_email(order, payment, user):
# #     mail_subject = 'Order Confirmation'
# #     message = render_to_string('order/order_confirmation_email.html', {
# #         'user': user,
# #         'order': order,
# #         'payment': payment,
# #     })
# #     to_email = user.email
# #     send_email = EmailMessage(mail_subject, message, to=[to_email])
# #     send_email.send()






from io import BytesIO
from unittest import result

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from order.invoice import USE_WEASY
from .models import Order, OrderProduct, Payment
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem, Coupon, DeliveryMethod
from store.models import Product, Variation
from django.core.mail import EmailMessage
from .forms import OrderForm, PaymentForm
from accounts.models import Account
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from django.conf import settings
from datetime import datetime


#  1. PLACE ORDER FUNCTION
@login_required(login_url='login')
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)

    if cart_items.count() <= 0:
        messages.warning(request, "Your cart is empty!")
        return redirect('store')

    total = sum(item.product.price * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)
    vat = total * Decimal('0.01')

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
    delivery_charge = 0
    delivery_method = None
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

                    # Generate unique order number
                    order_number = f"{datetime.now().strftime('%Y%m%d')}{order.id}"
                    order.order_number = order_number
                    order.save()

                    # Update coupon usage
                    if coupon:
                        coupon.used_count += 1
                        coupon.save()

                    # Save order id to session
                    request.session['order_id'] = order.id

                    #  Instead of render, redirect to payments
                    messages.success(request, "Order placed successfully! Please complete your payment.")
                    return redirect('payments')

            except Exception as e:
                messages.error(request, f"Error placing order: {str(e)}")
                return redirect('checkout')
        else:
            messages.error(request, "Invalid order form. Please check your details.")
            return redirect('checkout')

    return redirect('checkout')


# 2. PAYMENTS FUNCTION
@login_required(login_url='login')
def payments(request):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, "No order found. Please place your order first.")
        return redirect('checkout')

    try:
        order = Order.objects.get(id=order_id, user=request.user, is_ordered=False)
    except Order.DoesNotExist:
        messages.error(request, "Order not found or already completed.")
        return redirect('store')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    payment_method = form.cleaned_data['payment_method']
                    payment = Payment(
                        user=request.user,
                        payment_method=payment_method,
                        amount_paid=order.grand_total,
                        status='completed' if payment_method != 'cod' else 'pending'
                    )

                    # Save extra details based on payment method
                    if payment_method in ['bkash', 'nagad', 'rocket', 'upay']:
                        payment.mobile_number = form.cleaned_data.get('mobile_number')
                        payment.transaction_id = form.cleaned_data.get('transaction_id')

                    elif payment_method in ['card', 'emi']:
                        payment.card_number = form.cleaned_data.get('card_number')[-4:]
                        payment.card_holder_name = form.cleaned_data.get('card_holder_name')
                        if payment_method == 'emi':
                            payment.emi_month = form.cleaned_data.get('emi_month')

                    payment.save()

                    # Update order
                    order.payment = payment
                    order.is_ordered = True
                    order.status = 'Accepted' if payment_method != 'cod' else 'New'
                    order.save()

                    # Move cart items to OrderProduct
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

                        # Reduce stock
                        item.product.stock -= item.quantity
                        item.product.save()
                    cart_items.delete()

                    # Send confirmation email
                    send_order_confirmation_email(order, payment, request.user)

                    if 'order_id' in request.session:
                        del request.session['order_id']

                    messages.success(request, "Payment completed successfully!")

                    #  Redirect to order_complete with parameters
                    return redirect(f"{reverse('order_complete')}?order_id={order.order_number}&payment_id={payment.id}")


            except Exception as e:
                messages.error(request, f"Payment error: {str(e)}")
                return redirect('payments')
        else:
            messages.error(request, "Please correct the payment information.")
            return render(request, 'payment/payment.html', {'order': order, 'form': form})

    else:
        form = PaymentForm()
        return render(request, 'payment/payment.html', {'order': order, 'form': form})


# 3. ORDER COMPLETE FUNCTION
def order_complete(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_id, is_ordered=True)
        payment = Payment.objects.get(id=payment_id)
        order_products = OrderProduct.objects.filter(order=order)

        context = {
            'order': order,
            'payment': payment,
            'order_products': order_products,
        }
        return render(request, 'order/order_complete.html', context)
    except (Order.DoesNotExist, Payment.DoesNotExist):
        messages.error(request, "Order not found.")
        return redirect('store')


# 4. EMAIL FUNCTION (same as before)
def send_order_confirmation_email(order, payment, user):
    try:
        mail_subject = f'Order Confirmation - {order.order_number}'
        message = render_to_string('emails/order_confirmation.html', {
            'user': user,
            'order': order,
            'payment': payment,
        })
        email = EmailMessage(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.content_subtype = "html"
        email.send()
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'payment/order_history.html', context)

# 6. ORDER DETAIL
@login_required(login_url='login')
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_products = OrderProduct.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_products': order_products,
    }
    return render(request, 'payment/order_detail.html', context)


@login_required(login_url='login')
def invoice_cart_pdf(request):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('checkout')
    
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('store')
    billing = {
        'first_name': request.POST.get('first_name', ''),
        'last_name':  request.POST.get('last_name', ''),
        'email':      request.POST.get('email', ''),
        'phone':      request.POST.get('phone', ''),
        'address_line_1': request.POST.get('address_line_1', ''),
        'address_line_2': request.POST.get('address_line_2', ''),
        'city':       request.POST.get('city', ''),
        'state':      request.POST.get('state', ''),
        'country':    request.POST.get('country', ''),
        'order_note': request.POST.get('order_note', ''),
    }
    total = sum(item.product.price * item.quantity for item in cart_items)
    vat = total * Decimal('0.01')

    discount_amount = Decimal('0')
    coupon_code = None
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.is_valid(total):
                discount_amount = coupon.get_discount_amount(total)
                coupon_code = coupon.code
        except Coupon.DoesNotExist:
            pass
    
    # Delivery charge calculation
    delivery_charge = Decimal('0.00')
    delivery_method_id = request.session.get('delivery_method_id')
    if delivery_method_id:
        try:
            delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)
            delivery_charge = delivery_method.price
        except DeliveryMethod.DoesNotExist:
            delivery_charge = Decimal('0.00')

    grand_total = total + vat + delivery_charge - discount_amount
    context = {
        'user': user,
        'billing': billing,
        'cart_items': cart_items,
        'total': total,
        'vat': vat,
        'delivery_charge': delivery_charge,
        'discount_amount': discount_amount,
        'coupon_code': coupon_code,
        'grand_total': grand_total,
        'generated_at': timezone.now(),
    }
    html = render_to_string('order/invoice_cart.html', context)
    filename = f'invoice_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Try WeasyPrint first if allowed
    USE_WEASY = getattr(settings, "USE_WEASY", False)
    if USE_WEASY:
        try:
            from weasyprint import HTML
            HTML(string=html, base_url=request.build_absolute_uri("/")).write_pdf(response)
            return response
        except Exception as e:
            # Fallback silently to xhtml2pdf
            pass
    try:
        from xhtml2pdf import pisa
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("PDF generation error.", status=500)
        return response
    except Exception:
        return HttpResponse("PDF backend not available. Install WeasyPrint or xhtml2pdf.", status=500)


        











##############

def invoice_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    payment = order.payment
    order_products = OrderProduct.objects.filter(order=order).select_related('product').prefetch_related('variations')

    items = []
    subtotal = Decimal('0.00')
    for op in order_products:
        line_total = op.product_price * op.quantity
        subtotal += line_total
        items.append({
            "product": op.product,
            "quantity": op.quantity,
            "product_price": op.product_price,
            "line_total": line_total,
            "variations": list(op.variations.all()),
        })
    context = {
        "order": order,
        "payment": payment,
        "items": items,
        "subtotal": subtotal,
    }
    return render(request, "order/invoice.html", context)


def _render_pdf_from_html(request, template_name, context, filename):
    html = render_to_string(template_name, context)
    resp = HttpResponse(content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="{filename}"'

    
    if USE_WEASY:
        try:
            from weasyprint import HTML
        except ImportError:
             return HttpResponse(
                "PDF generation requires the 'WeasyPrint' package. Install it with: pip install WeasyPrint",
                content_type='text/plain',
                status=500
             )
        from io import BytesIO
        result = BytesIO()
        
        pisa_status = pisa.CreatePDF(src=html, dest=result)        
        if pisa_status.err:
            return HttpResponse(html, content_type='text/html')
        resp.write(result.getvalue())
        return resp




# --- A) Checkout পেজ থেকে Proforma/Cart Invoice ---
@login_required(login_url='login')
def download_cart_invoice(request):

    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('store')
    
    # same math as place_order()
    total = sum(item.product.price * item.quantity for item in cart_items)
    vat = total * Decimal('0.01')

    discount_amount = Decimal('0.00')
    coupon = None
    cid = request.session.get('coupon_id')
    if cid:
        try:
            coupon = Coupon.objects.get(id=cid)
            if coupon.is_valid(total):
                discount_amount = coupon.get_discount_amount(total)
        except Coupon.DoesNotExist:
            discount_amount = Decimal('0.00')
    delivery_charge = Decimal('0.00')
    delivery_method_id = request.session.get('delivery_method_id')
    if delivery_method_id:
        try:
            dm = DeliveryMethod.objects.get(id=delivery_method_id)
            delivery_charge = dm.price
        except DeliveryMethod.DoesNotExist:
            delivery_charge = Decimal('0.00')

    total_price = total + vat + delivery_charge - discount_amount

    ctx = {
        'order': None,
        'cart_items': cart_items,
        'user': request.user,
        'now': timezone.now(),
        'total': total,
        'vat': vat,
        'delivery_charge': delivery_charge,
        'discount_amount': discount_amount,
        'total_price': total_price,
    }
    filename = f"Proforma_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"
    return _render_pdf_from_html(request, 'order/invoice.html', ctx, filename)

@login_required(login_url='login')
def download_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user, is_ordered=True)
    order_products = OrderProduct.objects.filter(order=order)

    ctx = {
        'order': order,
        'order_products': order_products,
        'now': timezone.now(),
        'total': order.order_total,
        'vat': order.tax,
        'delivery_charge': order.delivery_charge,
        'discount_amount': order.discount,
        'total_price': order.grand_total,
    }

    filename = f"Invoice_{order.order_number}.pdf"
    return _render_pdf_from_html(request, 'order/invoice.html', ctx, filename)
    return _render_pdf_from_html(request, 'order/invoice.html', ctx, filename)
##################