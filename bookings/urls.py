from django.urls import path
from . import views 

urlpatterns = [
    path('', views.booking_portal, name='booking_portal'),
    path('success/', views.booking_success, name='booking_success'),
]