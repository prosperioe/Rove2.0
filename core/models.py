from django.db import models
from django.contrib.auth.models import User

#for consultation booking
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
    phone_number = models.CharField(max_length=20, blank=True)
    consultation_type = models.CharField(max_length=50, choices=CONSULTATION_TYPES)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    project_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending') # Pending, Confirmed, Completed

    class Meta:
        ordering = ['-preferred_date', '-preferred_time']

    def __str__(self):
        return f"{self.company_name} - {self.consultation_type} ({self.preferred_date})"
    

class SoftwareLicense(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    plan_tier = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, default='Paid')
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.plan_tier} ({self.email})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    career = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"