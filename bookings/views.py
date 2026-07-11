from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ConsultationForm

def booking_portal(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # --- The Manager Alert Payload ---
            # Set this to the email address where you want to receive booking alerts
            MANAGER_EMAIL = settings.EMAIL_HOST_USER 
            
            subject = f"URGENT: New Consultation Request - {booking.company_name}"
            message = (
                f"New booking received from {booking.contact_name} ({booking.company_name}).\n\n"
                f"--- OUTREACH DETAILS ---\n"
                f"Email: {booking.email}\n"
                f"WhatsApp: {booking.whatsapp_number}\n\n"
                f"--- AVAILABILITY MATRIX ---\n"
                f"Dates: {booking.available_start_date} to {booking.available_end_date}\n"
                f"Times: {booking.available_start_time} to {booking.available_end_time}\n\n"
                f"--- OBJECTIVE ---\n"
                f"{booking.project_description}\n\n"
                f"Log into the Admin Dashboard to respond."
            )
            
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [MANAGER_EMAIL], fail_silently=False)
            except Exception as e:
                print(f"Manager Alert Email Failed: {e}")

            messages.success(request, 'Your availability matrix has been logged. Our engineering manager will contact you shortly.')
            return redirect('booking_success')
    else:
        form = ConsultationForm()
        
    return render(request, 'bookings/portal.html', {'form': form})

def booking_success(request):
    return render(request, 'bookings/success.html')