from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import RegistationForm
from .models import Account
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
from django.urls import reverse
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
            username = email.split("@")[0]
            user = Account.object.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
#user activation
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/account_variafication_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            messages.success(request, 'Registation Successful.')
            """query_string = f"?command=verification_email&email={email_address}"
            return redirect('/account/login/' + query_string)"""

            email_string = "?command=verification&email={email}"
            return redirect('/account/login/' + email_string)

            
    else:
        form = RegistationForm()
    context = {
        'form' : form,
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
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
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
        if Account.object.filter(email=email).exists():
            user =Account.object.get(email__exact=email) #ai line a (__exact) aati r kaj hoitece amra pass reset korar jnno je email ta diyeci seta amader database a ace naki 
            
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
            user = Account.object.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'account/resetpassword.html')

