from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Example route
    path('index/',views.index,name="index"),
    path('first/',views.first,name="first"),
]
