from django.contrib import admin
from .models import Patient, OsmotrPatient, PatientImage


admin.site.register(Patient)
admin.site.register(OsmotrPatient)
admin.site.register(PatientImage)
