import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import ConsultationForm, InquiryForm

logger = logging.getLogger(__name__)


def booking_portal(request):
    active_tab = request.GET.get('tab', 'inquiry')
    consultation_form = ConsultationForm()
    inquiry_form = InquiryForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'inquiry')

        if form_type == 'inquiry':
            inquiry_form = InquiryForm(request.POST)
            active_tab = 'inquiry'
            if inquiry_form.is_valid():
                inquiry = inquiry_form.save()

                # ── 1. Alert Manager with inquiry_type in Subject Line ────────
                MANAGER_EMAIL = settings.EMAIL_HOST_USER
                manager_subject = f"New Inquiry: [{inquiry.inquiry_type}] — {inquiry.name}"
                manager_message = (
                    f"New Inquiry Received:\n\n"
                    f"Selected Option: {inquiry.inquiry_type}\n"
                    f"Sender Name:     {inquiry.name}\n"
                    f"Sender Email:    {inquiry.email}\n\n"
                    f"Message Details:\n{inquiry.message}\n\n"
                    f"Log into the admin dashboard to process this inquiry."
                )
                try:
                    send_mail(manager_subject, manager_message, settings.EMAIL_HOST_USER, [MANAGER_EMAIL], fail_silently=False)
                except Exception as e:
                    logger.error("Manager inquiry alert email failed: %s", e, exc_info=True)

                # ── 2. Send Feedback Confirmation to Client ────────────────────
                if inquiry.email:
                    client_subject = f"Response Recorded: {inquiry.inquiry_type}"
                    client_message = (
                        f"Hello {inquiry.name},\n\n"
                        f"Thank you for contacting ROVE regarding '{inquiry.inquiry_type}'.\n"
                        f"Your response has been recorded. Our team is reviewing your details and will get back to you shortly.\n\n"
                        f"Summary of your submission:\n"
                        f"Inquiry Type: {inquiry.inquiry_type}\n"
                        f"Message: {inquiry.message}\n\n"
                        f"Best regards,\n"
                        f"The ROVE Engineering Team"
                    )
                    try:
                        send_mail(
                            client_subject,
                            client_message,
                            settings.EMAIL_HOST_USER,
                            [inquiry.email],
                            fail_silently=False
                        )
                    except Exception as e:
                        logger.error("Client inquiry confirmation email failed: %s", e, exc_info=True)

                messages.success(request, 'Your response has been recorded. Our team will review your inquiry and reach out shortly.')
                return redirect('booking_success')

        elif form_type == 'consultation':
            consultation_form = ConsultationForm(request.POST)
            active_tab = 'consultation'
            if consultation_form.is_valid():
                booking = consultation_form.save()

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
                    logger.error("Manager consultation alert email failed: %s", e, exc_info=True)

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
                        logger.error("Client consultation confirmation email failed: %s", e, exc_info=True)

                messages.success(request, 'Your booking request has been received. Our team will be in touch within one business day.')
                return redirect('booking_success')

    return render(request, 'bookings/portal.html', {
        'consultation_form': consultation_form,
        'inquiry_form': inquiry_form,
        'active_tab': active_tab,
    })


def booking_success(request):
    return render(request, 'bookings/success.html')