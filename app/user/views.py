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
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

# User Authenticated     
def check_user_not_authenticated(user):
    return not user.is_authenticated


# Login
@user_passes_test(check_user_not_authenticated, login_url='/books/shelves', redirect_field_name=None)
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
            next_url = request.GET.get('next', 'shelves')
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
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect(reverse('login'))
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('shelves_book') 


# Sending Email
def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    domain = request.build_absolute_uri('/')[:-1]  
    #'domain': '192.168.178.100/', raspi
    #'domain': '127.0.0.1:8000/', localhost
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    protocol = 'https' if request.is_secure() else 'http'

    # Prepare the email content
    message = render_to_string("user/template_activate_account.html", {
        'user': user.username,
        'domain': domain,
        'uid': uid,
        'token': token,
        #"protocol": protocol not necessary the way i get the domain
    })

    email = EmailMessage(mail_subject, message, to=[to_email])
    
    try:
        if email.send():
            messages.success(request, f'Dear {user}, please check your email {to_email} for the activation link. Note: Check your spam folder.')
        else:
            messages.error(request, f'Failed to send email to {to_email}. Please check if the shelvesress is correct.')
    except Exception as e:
        logger.error(f"Error sending activation email to {to_email}: {e}")
        messages.error(request, 'An unexpected error occurred while sending the activation email.')


# Register
@user_passes_test(check_user_not_authenticated, login_url='/books/shelves', redirect_field_name=None)
def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email confirmation
            user.save()
            activateEmail(request, user, user.email)
            return redirect(reverse('login'))
        else:
            # Display form errors
            for error in form.errors.values():
                messages.error(request, error)
    
    return render(request, 'user/register.html', {
        'form': form,
        'active_page': 'register'
    })

# Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('login')) 
