from django.shortcuts import render
from carts.models import Cart, CartItem
from .forms import OrderForm
import datetime
# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_item = CartItem.object.filter(user=current_user)
    cart_count = cart_item.count()
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
            data.first_name = form.cleaned_data('first_name')
            data.last_name = form.cleaned_data('last_name')
            data.phone = form.cleaned_data('phone')
            data.email =form.cleaned_data('email')
            data.full_address = form.cleaned_data('full_address')
            data.city = form.cleaned_data('city')
            data.division = form.cleaned_data('division')
            data.area = form.cleaned_data('area')
            data.order_note = form.cleaned_data('order_note')
            data.order_total = total_price.cleaned_data('order_total')
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
            return redirect('checkout')
        
        else:
            return redirect('checkout')

            
            