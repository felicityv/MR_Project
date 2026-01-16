from django.urls import path
from . import views

urlpatterns = [
    path('registerpage/', views.register, name='register'),
    path('loginpage/', views.user_login, name='login'),
    path('logoutpage/', views.user_logout,name='logout'),
    path('profile/', views.profile, name='profile'),
]
