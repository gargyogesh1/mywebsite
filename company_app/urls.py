from django.urls import path
from . import views  # Import your views

urlpatterns = [
    

    # Add your URL patterns here
    path('company_register/', views.company_register,name='company_register'),
    path('company_login/',views.company_login,name="company_login"),
    path('company_forgot_password/',views.company_forgot_password,name="company_forgot_password"),
    path('company_profile/',views.company_profile,name="company_profile"),
    path('company_front/',views.company_front,name="company_front"),
    path('card/<id>/', views.card_detail, name='card_detail'),
    path('company_job/',views.company_job, name = 'company_job'),
    path('all_job_applications/', views.all_job_applications, name='all_job_applications'),
    path('job_applications/<id>', views.job_applications, name='job_applications'),
    path('update_job_status/<int:job_id>/', views.update_job_status, name='update_job_status'),

]
