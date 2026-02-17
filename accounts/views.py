from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm
from .models import User

import random
from django.core.mail import send_mail
from django.conf import settings

def register_view(request):
    """
    User registration view with OTP verification
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            
            # Store data in session
            request.session['register_data'] = form.cleaned_data
            # Remove password from cleaned_data before storing if needed, but we need it to create user later.
            # form.cleaned_data contains raw password.
            
            # Store OTP in session
            request.session['register_otp'] = otp
            
            # Send Email
            email = form.cleaned_data.get('email')
            subject = 'Verify your email - PetStore'
            message = f'Your OTP for registration is: {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            
            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, f'OTP sent to {email}. Please verify.')
                return redirect('accounts:verify_otp')
            except Exception as e:
                messages.error(request, f'Error sending email: {e}')
                return redirect('accounts:register')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def verify_otp(request):
    """
    Verify OTP and create account
    """
    if 'register_data' not in request.session or 'register_otp' not in request.session:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('accounts:register')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        generated_otp = request.session.get('register_otp')
        
        if entered_otp == generated_otp:
            # Create User
            data = request.session.get('register_data')
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password1']
            )
            if 'phone' in data and data['phone']:
                user.phone = data['phone']
            
            if 'full_name' in data and data['full_name']:
                user.first_name = data['full_name']
                
            user.save()
            
            # Clear session
            del request.session['register_data']
            del request.session['register_otp']
            
            # Auto-login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome, {user.username}! Your account has been verified.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'accounts/verify_otp.html')


from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    """
    User login view
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                if 'next' in request.GET:
                    return redirect(request.GET['next'])
                
                if user.is_staff or user.is_superuser:
                    return redirect('dashboard:dashboard')
                    
                return redirect('home')
            else:
                 messages.error(request, 'Invalid email/phone or password.')
        else:
            messages.error(request, 'Please check your inputs.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    """
    User profile view with update functionality
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile.html', context)
