from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SoftwareLicense, UserProfile, SaaSProject


def home(request):
    return render(request, 'core/home.html')


def products(request):
    projects = SaaSProject.objects.all().order_by('-created_at')
    return render(request, 'core/products.html', {'projects': projects})


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
