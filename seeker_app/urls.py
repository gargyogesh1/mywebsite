from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Add your URL patterns here
    path('seeker_register/', views.seeker_register, name='seeker_register'),
    path('jobs/', views.seeker_jobs, name='seeker_jobs'),
    path('view_applications/', views.view_applications, name='view_applications'),
    path('seeker_login/', views.seeker_login, name='seeker_login'),
    path('seeker_forgot_password/', views.seeker_forgot_password, name='seeker_forgot_password'),
    path('seeker_profile/',views.seeker_profile, name='seeker_profile'),
    path('delete_field/<str:field>/<int:pk>/', views.delete_field, name='delete_field'),
    path('card/<str:id>/', views.seeker_card_detail, name='seeker_card_detail'),
    path('view_job_card/<str:id>/', views.seeker_view_job_detail, name='seeker_view_job_detail'),
    path('job/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('job/<int:job_id>/apply/success/', views.job_detail_success, name='job_detail_success_page'),
    path('job/<int:job_id>/apply/already_applied/', views.job_detail_already_applied, name='already_applied_page'),
]
