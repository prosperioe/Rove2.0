from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import SoftwareLicense
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SoftwareLicense, UserProfile

def home(request):
    return render(request, 'core/home.html')

def products(request):
    # A robust 20-item ecosystem categorized for enterprise scale
    ecosystem = [
        # Category: Autonomous Agents
        {"name": "AgentOS Core", "category": "Agents", "desc": "The foundational operating system for autonomous digital workers.", "time": "2:15"},
        {"name": "SalesMind", "category": "Agents", "desc": "Outbound sales agent capable of cold outreach and meeting scheduling.", "time": "1:45"},
        {"name": "SupportNode", "category": "Agents", "desc": "L1/L2 technical support automation with deep documentation context.", "time": "3:10"},
        {"name": "ResearchCrawler", "category": "Agents", "desc": "Automated data harvesting and synthesis from unstructured web sources.", "time": "2:30"},
        {"name": "CodeWhisper", "category": "Agents", "desc": "Autonomous PR reviewer and codebase refactoring agent.", "time": "4:00"},
        
        # Category: Robotics
        {"name": "RoboCore", "category": "Robotics", "desc": "Unified kinematics engine for industrial swarm robotics.", "time": "5:20"},
        {"name": "WarehouseSwarm", "category": "Robotics", "desc": "Logistics routing system reducing floor collision by 84%.", "time": "3:15"},
        {"name": "DroneOps", "category": "Robotics", "desc": "Aerial surveillance and inventory scanning API.", "time": "2:50"},
        {"name": "MedAssist Bot", "category": "Robotics", "desc": "Precision handling software for clinical environments.", "time": "4:15"},
        {"name": "AutoAssembly", "category": "Robotics", "desc": "High-torque manufacturing arm control protocols.", "time": "6:00"},

        # Category: Neural Networks
        {"name": "VisionNet", "category": "Neural Networks", "desc": "Real-time optical character and object recognition.", "time": "1:30"},
        {"name": "NLP Cortex", "category": "Neural Networks", "desc": "Enterprise-grade natural language processing model.", "time": "2:45"},
        {"name": "PredictEngine", "category": "Neural Networks", "desc": "Supply chain and financial forecasting architecture.", "time": "3:20"},
        {"name": "AudioSense", "category": "Neural Networks", "desc": "Lossless speech-to-text and acoustic anomaly detection.", "time": "1:55"},
        {"name": "FraudShield", "category": "Neural Networks", "desc": "Pattern recognition network for transaction security.", "time": "2:10"},

        # Category: Enterprise Infrastructure
        {"name": "DataVault", "category": "Infrastructure", "desc": "Quantum-resistant encrypted storage architecture.", "time": "3:40"},
        {"name": "CloudEdge", "category": "Infrastructure", "desc": "Distributed computing framework for low-latency AI.", "time": "2:25"},
        {"name": "SecOps AI", "category": "Infrastructure", "desc": "Automated threat hunting and firewall management.", "time": "4:30"},
        {"name": "SyncMatrix", "category": "Infrastructure", "desc": "Multi-database synchronization and backup protocols.", "time": "1:50"},
        {"name": "Analytics Pro", "category": "Infrastructure", "desc": "High-density data visualization and reporting engine.", "time": "3:05"},
    ]
    
    return render(request, 'core/products.html', {'ecosystem': ecosystem})

def research(request):
    return render(request, 'core/research.html')

def company(request):
    return render(request, 'core/company.html')

def pricing(request):
    return render(request, 'core/pricing.html')


def checkout(request, plan):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        # 1. Log transaction
        SoftwareLicense.objects.create(
            name=name, 
            email=email, 
            plan_tier=plan.capitalize()
        )
        
        # 2. Compile the HTML Email
        subject = f"Welcome to ROVE - {plan.capitalize()} License Activation"
        
        # Pass the user's data into the HTML template
        html_message = render_to_string('core/email_welcome.html', {
            'name': name,
            'plan': plan.capitalize()
        })
        
        # Create a plain-text fallback for older email clients
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject, 
                plain_message, 
                settings.EMAIL_HOST_USER, 
                [email], 
                html_message=html_message, # This tells Django to send it as a branded HTML email
                fail_silently=False
            )
        except Exception as e:
            print(f"Email failed to send: {e}")

        return redirect('checkout_success')

    context = {'plan': plan.capitalize()}
    return render(request, 'core/checkout.html', context)

def checkout_success(request):
    return render(request, 'core/checkout_success.html')

#AUTHENTICATION & SECURE PORTAL

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # New Fields
        career = request.POST.get('career')
        country = request.POST.get('country')
        language = request.POST.get('language')
        
        if password != password_confirm:
            messages.error(request, "Security alert: Passwords do not match.")
            return redirect('register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, "Security alert: System ID already registered.")
            return redirect('register')
            
        # Securely create user and hash password
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create the extended profile
        UserProfile.objects.create(
            user=user,
            career=career,
            country=country,
            language=language
        )
        
        # Authenticate immediately to ensure session is valid
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('dashboard')
        
    return render(request, 'core/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate securely
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Access Denied: Invalid credentials. Check your capitalization.")
            return redirect('login')
            
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# The @login_required decorator acts as a firewall. 
# Anonymous users are bounced back to the login page.
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'core/dashboard.html')

