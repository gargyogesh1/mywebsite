from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your URL patterns here
    path('', views.example_view, name='example_view'),  # Example route
    path('seeker_register/', views.seeker_register, name='seeker_register'),
    path('seeker_login/', views.seeker_login, name='seeker_login'),
    path('seeker_profile/',views.seeker_profile, name='seeker_profile'),
    
    
]
