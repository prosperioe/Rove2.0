from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('research/', views.research, name='research'),
    path('company/', views.company, name='company'),
    path('pricing/', views.pricing, name='pricing'),
    path('checkout/<str:plan>/', views.checkout, name='checkout'),
    path('checkout-success/',views.checkout_success, name='checkout_success'),
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]