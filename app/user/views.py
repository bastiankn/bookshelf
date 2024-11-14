from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


# User Authenticated     
def check_user_not_authenticated(user):
    return not user.is_authenticated


# Login
@user_passes_test(check_user_not_authenticated, login_url='/books/add', redirect_field_name=None)
def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try authenticating by username first
        user = authenticate(request, username=identifier, password=password)
        
        # If authentication fails, try using email
        if user is None:
            user_by_email = User.objects.filter(email=identifier).first()
            if user_by_email:
                user = authenticate(request, username=user_by_email.username, password=password)
        
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'add_book')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'user/login.html', {
                'form_error': 'Invalid username or password.',
                'active_page': 'login'
            })
    else:
        return render(request, 'user/login.html', {'active_page': 'login'})

# User Activation
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('/users/login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('add_book') 


# Sending Email
def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("user/template_activate_account.html", {
        'user': user.username,
        #'domain': '192.168.178.100/',
        'domain': '127.0.0.1:8000/',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'http' #if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
                received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


# Register
@user_passes_test(check_user_not_authenticated, login_url='/', redirect_field_name=None) # add redirect
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, user.email)
            return redirect('/users/login')  
    else:
        form = CustomUserCreationForm()
        for error in list(form.errors.values()):
            messages.error(request, error)
    return render(request, 'user/register.html', {'form': form,'active_page': 'register'})

# Logout
def logout_view(request):
    logout(request)
    return redirect('/users/login') # add redirect
