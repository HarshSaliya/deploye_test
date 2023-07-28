from .import views
from django.urls import path ,include



urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/',views.signupview),
    path('otp/' , views.otpview ,name='otp')
]