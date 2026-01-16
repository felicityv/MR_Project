from django import forms
from patient.models import OsmotrPatient, Patient
from mkb10.models import MKB10
from datetime import date
from django.utils import timezone

class OsmotrPatientForm(forms.ModelForm):
    on_date = forms.DateField(
        label='Дата осмотра',
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = OsmotrPatient
        fields = ['on_date', 'rost', 'ves']
        labels = {
            'rost': 'Рост (см)',
            'ves': 'Вес (кг)',
        }
        widgets = {
            'rost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'ves': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class PatientForm(forms.ModelForm):
    kod_mkb = forms.ModelChoiceField(
        queryset=MKB10.objects.all(),
        label='Диагноз по МКБ-10',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'data-live-search': 'true'
        })
    )

    class Meta:
        model = Patient
        fields = [
            'surname', 'name', 'data_birth', 'gender',
            'kod_mkb', 'diagnoz_osn', 'diagnoz_sop',
            'rost', 'ves', 'foto'
        ]
        labels = {
            'surname': 'Фамилия',
            'name': 'Имя',
            'data_birth': 'Дата рождения',
            'gender': 'Пол',
            'diagnoz_osn': 'Основной клинико-функциональный диагноз',
            'diagnoz_sop': 'Сопутствующий клинико-функциональный диагноз',
            'rost': 'Рост (см)',
            'ves': 'Вес (кг)',
            'foto': 'Фото',
        }
        widgets = {
            'data_birth': forms.DateInput(format='%Y-%m-%d',
                                        attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'diagnoz_osn': forms.Textarea(attrs={'class': 'form-control',
                                               'rows': 4}),
            'diagnoz_sop': forms.Textarea(attrs={'class': 'form-control',
                                               'rows': 4}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        patient = super().save(commit=False)
        if commit:
            patient.save()
            # создаём первичный осмотр
            OsmotrPatient.objects.create(
                patient=patient,
                data_osmotra=timezone.localdate(),
                rost=self.cleaned_data.get('rost'),
                ves=self.cleaned_data.get('ves'),
                mkb=self.cleaned_data.get('kod_mkb')
            )
        return patient
