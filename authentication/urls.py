from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your URL patterns here
    
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/', views.google_login, name='google_login'),
]
