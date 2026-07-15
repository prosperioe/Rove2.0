from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import ConsultationForm


def booking_portal(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # ── 1. Alert the ROVE manager ──────────────────────────────
            MANAGER_EMAIL = settings.EMAIL_HOST_USER
            manager_subject = f"New Consultation Request — {booking.company_name}"
            manager_message = (
                f"New booking from {booking.contact_name} ({booking.company_name}).\n\n"
                f"Contact Details:\n"
                f"  Email: {booking.email}\n"
                f"  WhatsApp: {booking.whatsapp_number}\n\n"
                f"Availability:\n"
                f"  Dates: {booking.available_start_date} → {booking.available_end_date}\n"
                f"  Times: {booking.available_start_time} → {booking.available_end_time}\n\n"
                f"Project Goals:\n{booking.project_description}\n\n"
                f"Log into the admin dashboard to respond."
            )
            try:
                send_mail(manager_subject, manager_message, settings.EMAIL_HOST_USER, [MANAGER_EMAIL], fail_silently=False)
            except Exception as e:
                print(f"Manager alert email failed: {e}")

            # ── 2. Send confirmation email to the client ───────────────
            if booking.email:
                client_subject = "Your ROVE Consultation Request Has Been Received"
                client_html = render_to_string('bookings/email_booking_confirmation.html', {
                    'name': booking.contact_name,
                    'company': booking.company_name,
                    'consultation_type': booking.get_consultation_type_display() if hasattr(booking, 'get_consultation_type_display') else booking.consultation_type,
                    'start_date': booking.available_start_date,
                    'end_date': booking.available_end_date,
                    'start_time': booking.available_start_time,
                    'end_time': booking.available_end_time,
                })
                client_plain = strip_tags(client_html)
                try:
                    send_mail(
                        client_subject,
                        client_plain,
                        settings.EMAIL_HOST_USER,
                        [booking.email],
                        html_message=client_html,
                        fail_silently=False
                    )
                except Exception as e:
                    print(f"Client confirmation email failed: {e}")

            messages.success(request, 'Your booking has been received. Our team will be in touch within one business day.')
            return redirect('booking_success')
    else:
        form = ConsultationForm()

    return render(request, 'bookings/portal.html', {'form': form})


def booking_success(request):
    return render(request, 'bookings/success.html')