from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
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
    ecosystem = [
        # Autonomous Agents
        {"name": "AgentOS Core", "category": "Agents", "desc": "The foundational operating system for autonomous digital workers — built to run 24/7 without supervision.", "time": "2:15"},
        {"name": "SalesMind", "category": "Agents", "desc": "An outbound sales agent that handles cold outreach, follow-ups, and meeting scheduling automatically.", "time": "1:45"},
        {"name": "SupportNode", "category": "Agents", "desc": "L1/L2 technical support automation with deep documentation context and escalation logic.", "time": "3:10"},
        {"name": "ResearchCrawler", "category": "Agents", "desc": "Automated data harvesting and synthesis from unstructured web sources — hours of research in seconds.", "time": "2:30"},
        {"name": "CodeWhisper", "category": "Agents", "desc": "An autonomous code reviewer and refactoring agent that keeps your codebase clean and efficient.", "time": "4:00"},

        # Robotics
        {"name": "RoboCore", "category": "Robotics", "desc": "A unified kinematics engine for coordinating industrial swarms of robots across large facilities.", "time": "5:20"},
        {"name": "WarehouseSwarm", "category": "Robotics", "desc": "Intelligent logistics routing that reduces floor collision incidents by up to 84%.", "time": "3:15"},
        {"name": "DroneOps", "category": "Robotics", "desc": "Aerial surveillance and real-time inventory scanning API for warehouse environments.", "time": "2:50"},
        {"name": "MedAssist Bot", "category": "Robotics", "desc": "Precision handling software designed specifically for clinical and surgical environments.", "time": "4:15"},
        {"name": "AutoAssembly", "category": "Robotics", "desc": "High-torque manufacturing arm control protocols for automated production lines.", "time": "6:00"},

        # Neural Networks
        {"name": "VisionNet", "category": "Neural Networks", "desc": "Real-time optical character recognition and object detection — accurate at any scale.", "time": "1:30"},
        {"name": "NLP Cortex", "category": "Neural Networks", "desc": "Enterprise-grade natural language processing model for document analysis and conversation.", "time": "2:45"},
        {"name": "PredictEngine", "category": "Neural Networks", "desc": "Supply chain and financial forecasting architecture trained on your proprietary data.", "time": "3:20"},
        {"name": "AudioSense", "category": "Neural Networks", "desc": "Lossless speech-to-text transcription with acoustic anomaly detection built in.", "time": "1:55"},
        {"name": "FraudShield", "category": "Neural Networks", "desc": "Pattern recognition network for real-time transaction monitoring and fraud detection.", "time": "2:10"},

        # Enterprise Infrastructure
        {"name": "DataVault", "category": "Infrastructure", "desc": "Quantum-resistant encrypted storage architecture for sensitive enterprise data.", "time": "3:40"},
        {"name": "CloudEdge", "category": "Infrastructure", "desc": "Distributed computing framework purpose-built for low-latency AI inference at the edge.", "time": "2:25"},
        {"name": "SecOps AI", "category": "Infrastructure", "desc": "Automated threat hunting and intelligent firewall management — security that never sleeps.", "time": "4:30"},
        {"name": "SyncMatrix", "category": "Infrastructure", "desc": "Multi-database synchronisation and automated backup protocols across hybrid environments.", "time": "1:50"},
        {"name": "Analytics Pro", "category": "Infrastructure", "desc": "High-density data visualisation and real-time reporting engine for executive decision-making.", "time": "3:05"},
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

        # Log the transaction
        SoftwareLicense.objects.create(
            name=name,
            email=email,
            plan_tier=plan.capitalize()
        )

        # Send license confirmation email to the buyer
        subject = f"Your ROVE {plan.capitalize()} License — Access Your Downloads"
        html_message = render_to_string('core/email_welcome.html', {
            'name': name,
            'plan': plan.capitalize()
        })
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [email],
                html_message=html_message,
                fail_silently=False
            )
        except Exception as e:
            print(f"License email failed to send: {e}")

        return redirect('checkout_success')

    context = {'plan': plan.capitalize()}
    return render(request, 'core/checkout.html', context)


def checkout_success(request):
    return render(request, 'core/checkout_success.html')


# ─── AUTHENTICATION & SECURE PORTAL ───────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        career = request.POST.get('career')
        country = request.POST.get('country')
        language = request.POST.get('language')

        if password != password_confirm:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken. Please choose another.")
            return redirect('register')

        # Create user and profile
        user = User.objects.create_user(username=username, email=email, password=password)

        UserProfile.objects.create(
            user=user,
            career=career,
            country=country,
            language=language
        )

        # Send welcome email to the new user
        if email:
            subject = "Welcome to ROVE — Your Account is Ready"
            html_message = render_to_string('core/email_registration.html', {
                'name': username,
            })
            plain_message = strip_tags(html_message)
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    html_message=html_message,
                    fail_silently=False
                )
            except Exception as e:
                print(f"Registration email failed to send: {e}")

        # Log in immediately
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

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password. Please check your credentials and try again.")
            return redirect('login')

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'core/dashboard.html')
