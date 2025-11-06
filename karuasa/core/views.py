from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import SliderImage, Partner, Testimonial, SiteInfo, Leader, ContactMessage
from events.models import Event
from projects.models import Project
from .forms import ContactForm, TestimonialForm
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import requests
from .models import Constitution
from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
    # Use try-except to handle cases where models aren't migrated yet
    try:
        sliders = SliderImage.objects.filter(is_active=True).order_by('created_at')
        partners = Partner.objects.filter(is_active=True)
        testimonials = Testimonial.objects.filter(is_approved=True)
        
        # Get upcoming events (events with future dates)
        upcoming_events = Event.objects.filter(
            is_active=True, 
            event_type='upcoming',
            date__gte=timezone.now()
        ).order_by('date')[:3]  # Limit to 3 events
        
        # Get featured projects
        featured_projects = Project.objects.filter(
            is_approved=True,
            is_featured=True
        ).order_by('-created_at')[:2]  # Limit to 2 featured projects
        
    except Exception as e:
        print(f"Error loading data: {e}")
        sliders = []
        partners = []
        testimonials = []
        upcoming_events = []
        featured_projects = []
    
    context = {
        'sliders': sliders,
        'partners': partners,
        'testimonials': testimonials,
        'upcoming_events': upcoming_events,
        'featured_projects': featured_projects,
    }
    return render(request, 'home.html', context)

def about_us(request):
    try:
        about_content = SiteInfo.objects.first()  # Rename to match template
        leaders = Leader.objects.filter(is_active=True)
        constitution = Constitution.objects.filter(is_active=True).first()
    except Exception as e:
        print(f"Error loading data: {e}")
        about_content = None  # Rename this too
        leaders = []
        constitution = None
    
    context = {
        'about_content': about_content,  # Change 'site_info' to 'about_content'
        'leaders': leaders,
        'constitution': constitution,
    }
    return render(request, 'core/about_us.html', context)
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # For now, just show success message without sending email
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})

def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            if request.user.is_authenticated:
                testimonial.author = f"{request.user.first_name} {request.user.last_name}"
            testimonial.save()
            messages.success(request, 'Thank you for your testimonial! It will be reviewed before publishing.')
            return redirect('home')
    else:
        form = TestimonialForm()
    
    return render(request, 'core/submit_testimonial.html', {'form': form})

# In your views.py
from .models import Constitution

def constitution_view(request):
    constitution = Constitution.objects.filter(is_active=True).first()
    context = {
        'constitution': constitution,
    }
    return render(request, 'constitution.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def is_admin(user):
    return user.is_staff or user.is_superuser

# Admin Message List
@login_required
@user_passes_test(is_admin)
def admin_message_list(request):
    contact_messages = ContactMessage.objects.all()
    return render(request, 'admin/message_list.html', {'messages': contact_messages})

# Admin Message Detail
@login_required
@user_passes_test(is_admin)
def admin_message_detail(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    # Mark as read when admin views it
    if message.status == 'unread':
        message.status = 'read'
        message.save()
    
    return render(request, 'admin/message_detail.html', {'message': message})




import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def chatbot_api(request):
    try:
        # Get the message from POST data
        user_message = request.POST.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Enhanced prompt for actuarial focus
        prompt = f"""You are KARUASA Assistant, a helpful AI for the Karatina University Actuarial Students Association. 
        
About KARUASA: We are the Karatina University Actuarial Students Association, dedicated to empowering future actuaries through excellence and innovation.

Your expertise covers:
- Actuarial science concepts, principles, and methodologies
- Professional actuarial exams (SOA, CAS, IFoA)
- Programming for actuaries (Python, R, SQL, Excel)
- Mathematics, statistics, and probability
- Economics, finance, and risk management
- Career guidance in the actuarial field
- Study tips, resources, and exam preparation strategies
- Professional development and networking
- Motivational support for actuarial students

Important guidelines:
- Be encouraging, professional, and supportive
- Provide accurate, practical information
- Focus on educational value
- Keep responses clear and concise
- If you don't know something, admit it and suggest resources
- Always maintain a positive and helpful tone

User question: {user_message}

Please provide a helpful response that would benefit actuarial students."""

        # Check if API key is configured
        if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
            return JsonResponse({
                'response': 'I apologize, but the AI assistant is currently being configured. Please check back later or contact the administrator.'
            })

        # CORRECT model name (remove "models/" prefix)
        model_name = "gemini-2.0-flash"  # Just the model name, not "models/gemini-2.0-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
        
        print(f"Attempting to call Gemini API with model: {model_name}")
        print(f"API URL: {url.split('?')[0]}")  # Print without API key for security
        
        # Make request to Gemini API
        response = requests.post(
            url,
            json={
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            },
            headers={
                'Content-Type': 'application/json',
            },
            timeout=30  # 30 second timeout
        )
        
        response.raise_for_status()  # This will raise an exception for bad status codes
        
        data = response.json()
        
        # Check if we have a valid response structure
        if (data.get('candidates') and 
            len(data['candidates']) > 0 and 
            data['candidates'][0].get('content') and 
            data['candidates'][0]['content'].get('parts') and 
            len(data['candidates'][0]['content']['parts']) > 0):
            
            bot_response = data['candidates'][0]['content']['parts'][0]['text']
            print(f"Successfully received response from Gemini API")
            return JsonResponse({'response': bot_response})
            
        else:
            print(f"Unexpected response structure: {data}")
            return JsonResponse({
                'response': 'I received an unexpected response format. Please try again.'
            })
            
    except requests.exceptions.Timeout:
        print("Gemini API request timed out")
        return JsonResponse({
            'response': 'The request timed out. Please try again in a moment.'
        })
    except requests.exceptions.RequestException as e:
        print(f"Gemini API request error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response status: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
            
        return JsonResponse({
            'response': 'I apologize, but I\'m having trouble connecting to the AI service right now. Please try again later.'
        })
    except Exception as e:
        print(f"Unexpected error in chatbot_api: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'response': 'An unexpected error occurred. Please try again later.'
        })