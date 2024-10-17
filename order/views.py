from django.shortcuts import render, redirect
from carts.models import Cart, CartItem
from .forms import OrderForm
from .models import Order, Payment , OrderProduct
import datetime
# Create your views here.

#payment method Start:
def payments(request, total=0, quantity=0 ):
    return render(request, 'payment/payment.html')
#payments method end



def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:

        return redirect('store')

    #tax ar jnno kicu code likhbo:
    vat = 0
    total_price = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    vat = (1 * total)/100
    total_price = total + vat # akn a je vat dilam aita ke amra niche ar ai app a models.py a tax hisabe dorci


    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all the billing information in order
            # amra checkout.html a ja ja nibo jeguli akn a dibo
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
            # data.order_total = total_price.cleaned_data['order_total']
            data.order_total = total_price
            data.tax = vat
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


            # Start Pyament Method
            # end payment method
            order = Order.objects.get(user=current_user, is_ordered=False,order_number=order_number)
            context = { #payment method kete dileo ai line takbe kintu
                'order' : order, #payment method kete dileo ai line takbe kintu
                'cart_items' : cart_items, #payment method kete dileo ai line takbe kintu
                'total' : total, #payment method kete dileo ai line takbe kintu
                'vat' : vat, #payment method kete dileo ai line takbe kintu
                'total_price' : total_price #payment method kete dileo ai line takbe kintu
            }
            #end payment method
            
            
            return render(request, 'payment/payment.html', context)
        
        else:
            return redirect('checkout')

            
            