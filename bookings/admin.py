from django.contrib import admin
from django.utils.html import format_html
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_name', 'date_range', 'time_range', 'status', 'contact_actions')
    list_filter = ('status', 'consultation_type')
    search_fields = ('company_name', 'email', 'contact_name', 'whatsapp_number')
    readonly_fields = ('created_at',)

    # Custom Column: Display the date range cleanly
    def date_range(self, obj):
        return f"{obj.available_start_date} to {obj.available_end_date}"
    date_range.short_description = 'Availability Window'

    # Custom Column: Display the time range cleanly
    def time_range(self, obj):
        return f"{obj.available_start_time.strftime('%H:%M')} - {obj.available_end_time.strftime('%H:%M')}"
    time_range.short_description = 'Daily Time Window'

    # Custom Column: Clickable WhatsApp and Email buttons
    def contact_actions(self, obj):
        # Clean the number to ensure the WhatsApp API works (remove spaces/dashes)
        clean_phone = ''.join(filter(str.isalnum, obj.whatsapp_number))
        return format_html(
            '<a class="button" style="background-color:#25D366; color:white; font-weight:bold; margin-right:5px;" href="https://wa.me/{}" target="_blank">WhatsApp</a>&nbsp;'
            '<a class="button" style="background-color:#007BFF; color:white; font-weight:bold;" href="mailto:{}">Email</a>',
            clean_phone, obj.email
        )
    contact_actions.short_description = 'Outreach'