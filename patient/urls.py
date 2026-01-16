from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_create, name='patient_add'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/delete/', views.patient_delete, name='patient_delete'),
    path('patients/<int:patient_id>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:patient_id>/osmotr/add/', views.osmotr_add, name='osmotr_add'),
    path('osmotr/<int:osmotr_id>/delete/', views.osmotr_delete, name='osmotr_delete'),
    path('osmotr/<int:osmotr_id>/edit/', views.osmotr_edit, name='osmotr_edit'),
]
