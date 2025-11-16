# ai views.py er backend code 15-11-2025 a views_by_me.py file a ace error
#asle change kore nio 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .forms import RegistationForm
from .models import Account
from core.views import home
from carts.views import _cart_id
from carts.models import Cart, CartItem
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
#aita email variafication ar library:
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from collections import OrderedDict
from order.models import Order
# Create your views here.

#customize:

def register(request):
    if request.method == 'POST':
        form = RegistationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            # -------- FIX START --------
            # Base username from email prefix
            base_username = email.split("@")[0]
            username = base_username

            # If username exists, add numbers (sadik, sadik1, sadik2 ...)
            counter = 1
            while Account.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            # -------- FIX END --------

            # Create user with unique username
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )

            # Add phone number & save
            user.phone_number = phone_number
            user.is_active = False 
            user.save()

            # ----- Email Verification -----
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/account_variafication_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Registration successful! Please check your email to verify your account.')

            return redirect('/account/login/?verification=sent')

    else:
        form = RegistationForm()

    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context)

#login:
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f"Email: {email}, Password: {password}")
        user= auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))
                    # get the cart items from the user to access his product variation
                    cart_item = CartItem.objects.filter(user=user)
                    existing_variation_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        existing_variation_list.append(list(existing_variation))
                        id.append(item.id)
                    #     item.user = user
                    #     item.save()
                    for pr in product_variation:
                        if pr in existing_variation_list:
                            index = existing_variation_list.index(pr)
                            item_id=id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                user.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            
            url = request.META.get('HTTP_REFERER') # HTTP_REFERER will do is it will just grap the previous url from where you came
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
            # return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'account/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out.')
    return redirect('login')
    # return render(request, 'account/logout.html')

# email token activate
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your Account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

#dashboard:
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'account/dashboard.html')

#Forgot Password:
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user =Account.objects.get(email__exact=email) #ai line a (__exact) aati r kaj hoitece amra pass reset korar jnno je email ta diyeci seta amader database a ace naki 
            
            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password.'
            message = render_to_string('account/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            send_email.send()
            messages.success(request,'Password reset email has been sent on your email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotpassword')
    return render(request, 'account/forgot_password.html')

#resetpassword_validate
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Password.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expried') 
        return redirect('login')

#resetpassword
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'account/resetpassword.html')

# def home(request):
#     return render(request, 'index.html')
@login_required(login_url='login')
# def profile(request):
#     user = request.user
#     orders = Order.objects.filter(user=user).values(
#         'first_name', 'last_name', 'phone', 'email',
#         'address_line_1', 'address_line_2',
#         'city', 'state', 'country', 'postal_code'

#     ).distinct()
#     context = {
#         'user': user,
#         'addresses': orders
#     }   
#     return render(request, 'account/profile.html', context)
def profile(request):
    #
    user = request.user
    orders = Order.objects.filter(
        user=user, is_ordered=True
    ).order_by('-created_at')
    unique_addresses = OrderedDict()
    for order in orders:
        addr_keys  = f"{order.address_line_1}|{order.address_line_2}|{order.city}|{order.state}|{order.country}|{order.phone}"

        if addr_keys not in unique_addresses:
            unique_addresses[addr_keys] = order
    
    default_address = None
    if unique_addresses:
        default_address = list(unique_addresses.values())[0]
        context = {
            'user': user,
            'addresses': unique_addresses.values(),  # merged
            'default_address': default_address,       # for highlight
        }
        return render(request, 'account/profile.html', context)












    # # ========= 1) UNIQUE ADDR
    
    # #  POST request jnno (form update  )
    # if request.method == 'POST':
    #     # akn a profile update logic implement korechi
    #     first_name = request.POST.get('first_name')
    #     last_name = request.POST.get('last_name')
    #     email = request.POST.get('email')
    #     phone_number = request.POST.get('phone_number')
        
    #     # User data update
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.email = email
    #     user.phone_number = phone_number
    #     user.save()
        
    #     messages.success(request, 'Profile updated successfully!')
    #     return redirect('profile')
    
    # context = {
    #     'user': user,
    # }
    # return render(request, 'account/profile.html', context)