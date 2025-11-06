import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import Member
from .forms import MemberRegistrationForm, MemberUpdateForm

def members_list(request):
    """Display list of all active members"""
    members = Member.objects.filter(is_active=True).order_by('-date_joined')
    context = {
        'members': members,
        'total_members': members.count()
    }
    return render(request, 'members/members_list.html', context)

def register(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send welcome email
            send_welcome_email(user)
            
            messages.success(request, 'Registration successful! Please login to access your account.')
            return redirect('members:login')  # Redirect to login page immediately
            
    else:
        form = MemberRegistrationForm()
    
    return render(request, 'members/register.html', {'form': form})

def member_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    
    return render(request, 'members/login.html')

def member_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = MemberUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('members:profile')
    else:
        form = MemberUpdateForm(instance=request.user)
    
    return render(request, 'members/profile.html', {'form': form})

def send_welcome_email(member):
    subject = 'Welcome to KARUASA!'
    message = f'''
    Dear {member.first_name},
    
    Welcome to the Karatina University Actuarial Students Association!
    
    Your registration is now complete. You can now access all member benefits including:
    - Learning resources
    - Project collaborations
    - Competition participation
    - Career development opportunities
    
    Login to your dashboard to get started: https://yourdomain.com/dashboard/
    
    Best regards,
    KARUASA Team
    '''
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [member.email]
    
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send welcome email: {e}")