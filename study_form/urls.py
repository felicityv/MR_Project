from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_form, name='form'),     
    path('django_form/', views.get_django_form, name='django_form'),
]
