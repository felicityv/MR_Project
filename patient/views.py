from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from patient.models import Patient


def patient_list(request):
    """Выводит список всех пациентов"""
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def patient_detail(request, id):
    """Выводит карточку конкретного пациента"""
    patient = get_object_or_404(Patient, id=id)
    return render(request, 'patient_detail.html', {'patient': patient})