# bookings/forms.py
from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = [
            'consultation_type', 'company_name', 'contact_name', 'email', 'whatsapp_number',
            'available_start_date', 'available_end_date', 'available_start_time', 'available_end_time', 'project_description'
        ]
        
        input_classes = 'w-full p-3 bg-gray-50 dark:bg-[#111] border border-gray-200 dark:border-gray-800 rounded-lg focus:ring-2 focus:ring-brand-light outline-none text-gray-900 dark:text-white'
        
        widgets = {
            'consultation_type': forms.Select(attrs={'class': input_classes}),
            'company_name': forms.TextInput(attrs={'class': input_classes}),
            'contact_name': forms.TextInput(attrs={'class': input_classes}),
            'email': forms.EmailInput(attrs={'class': input_classes}),
            'whatsapp_number': forms.TextInput(attrs={'class': input_classes, 'placeholder': '+234...'}),
            'available_start_date': forms.DateInput(attrs={'type': 'date', 'class': input_classes}),
            'available_end_date': forms.DateInput(attrs={'type': 'date', 'class': input_classes}),
            'available_start_time': forms.TimeInput(attrs={'type': 'time', 'class': input_classes}),
            'available_end_time': forms.TimeInput(attrs={'type': 'time', 'class': input_classes}),
            'project_description': forms.Textarea(attrs={'rows': 4, 'class': input_classes, 'placeholder': 'Describe your primary objectives...'}),
        }