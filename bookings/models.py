from django.db import models

class Consultation(models.Model):
    CONSULTATION_TYPES = [
        ('AI Strategy', 'AI Strategy Consultation'),
        ('Robotics', 'Robotics Consultation'),
        ('Product Demo', 'Product Demo'),
        ('Technical Discovery', 'Technical Discovery Session'),
        ('Investor Meeting', 'Investor Meeting'),
        ('Research Collaboration', 'Research Collaboration'),
    ]

    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=150)
    email = models.EmailField()
    whatsapp_number = models.CharField(max_length=20, help_text="Include country code, e.g., +234...")
    
    consultation_type = models.CharField(max_length=50, choices=CONSULTATION_TYPES)
    
    # The Availability Matrix
    available_start_date = models.DateField(verbose_name="Available From Date")
    available_end_date = models.DateField(verbose_name="Available Until Date")
    available_start_time = models.TimeField(verbose_name="Available From Time")
    available_end_time = models.TimeField(verbose_name="Available Until Time")
    
    project_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending') 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} - {self.consultation_type}"


class Inquiry(models.Model):
    INQUIRY_TYPES = [
        ("Collaborate on a project", "Collaborate on a project"),
        ("Invest in my software", "Invest in my software"),
        ("Buy a software license", "Buy a software license"),
        ("Ask for technical help", "Ask for technical help"),
        ("Hire me for contract work", "Hire me for contract work"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    inquiry_type = models.CharField(max_length=100, choices=INQUIRY_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.inquiry_type}"