from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your URL patterns here
    path('seeker_register/', views.seeker_register, name='seeker_register'),
    path('jobs/', views.seeker_jobs, name='seeker_jobs'),
    path('seeker_login/', views.seeker_login, name='seeker_login'),
    path('seeker_forgot_password/', views.seeker_forgot_password, name='seeker_forgot_password'),
    path('seeker_profile/',views.seeker_profile, name='seeker_profile'),
    path('delete_field/<str:field>/<int:pk>/', views.delete_field, name='delete_field'),
]
