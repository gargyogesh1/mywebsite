from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your URL patterns here
    path('', views.example_view, name='example_view'),
    
    path('company_register/', views.company_register,name='company_register'),
    path('company_login/',views.company_login,name="company_login"),
    path('company_profile/',views.company_profile,name="company_profile"),
    path('company_front/',views.company_front,name="company_front"),

    path('card/<unique_number>/', views.card_detail, name='card_detail'),

    path('company_job/',views.company_job, name = 'company_job'),
    # Example route
]
