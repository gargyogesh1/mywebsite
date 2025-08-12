from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include , re_path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('seeker_app/',include('seeker_app.urls')),
    path('company_app/',include('company_app.urls')),
    path('authentication/',include('authentication.urls')),
    path('job_finder/',include('job_finder.urls')),
    
    path('',views.default_page,name='default_page'),
    path('home/', views.home, name='home'),
    path('common/', views.common, name='common'),
    path('success/', views.success, name='success'),
    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<int:user_id>/<str:token>/', views.reset_password, name='reset_password'),
    
    # path('company_register/', views.company_register,name='company_register'),
    # path('company_login/',views.company_login,name="company_login"),
    path("__reload__/", include("django_browser_reload.urls")),

    re_path(r'.*/logout/$', views.logout_view, name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)