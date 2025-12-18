from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .models import Patient, OsmotrPatient,PatientImage


def patient_list(request):
    patients = Patient.objects.all()
    context = {
    'patients': patients,
    }
    return render(request, 'patient_list.html', context)

def patient_detail(request, id):
    patient = get_object_or_404(Patient, id=id)
    osmotry = OsmotrPatient.objects.filter(patient=patient).order_by('-data_osmotra')
    images = PatientImage.objects.filter(patient=patient)
    context = {
    'patient': patient,
    'osmotry': osmotry,
    'images': images,
    }
    return render(request, 'patient_detail.html', context)



