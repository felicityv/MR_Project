from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Patient, OsmotrPatient, PatientImage
from .forms import PatientForm, OsmotrPatientForm
import logging

logger = logging.getLogger(__name__)   # включаем лог-вывод

# список пациентов
def patient_list(request):
    patients = Patient.objects.all()
    logger.info('Загружен список пациентов, всего: %s', patients.count())
    return render(request, 'patient_list.html', {'patients': patients})

# карточка пациента
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    osmotry = OsmotrPatient.objects.filter(patient=patient).order_by('-data_osmotra')
    last_osmotr = osmotry.first()
    images = PatientImage.objects.filter(patient=patient)
    form = OsmotrPatientForm()
    return render(request, 'patient_detail.html', {
        'patient': patient,
        'osmotry': osmotry,
        'last_osmotr': last_osmotr,   # ← передаём в шаблон
        'images': images,
        'form': form,
    })

# создание нового пациента
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save()
            logger.info('Создан пациент id=%s', patient.id)
            return redirect('patients:patient_detail', patient_id=patient.pk)
        else:
            logger.warning('Ошибки формы создания: %s', form.errors)
    else:
        form = PatientForm()
    return render(request, 'patient_form.html', {'form': form})

# редактирование пациента
def patient_edit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            # ставим дату последнего осмотра (или сейчас, если осмотров нет)
            last_osmotr = patient.osmotrpatient_set.order_by('-data_osmotra').first()
            patient.data_osmotra = last_osmotr.data_osmotra if last_osmotr else timezone.now()
            patient.save()
            logger.info('ОТРЕДАКТИРОВАН пациент id=%s, дата осмотра=%s',
                        patient.id, patient.data_osmotra)
            messages.success(request, 'Данные сохранены.')
            return redirect('patients:patient_detail', patient_id=patient.pk)
        else:
            logger.warning('Ошибки формы редактирования: %s', form.errors)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_form.html', {'form': form, 'patient': patient})

# удаление пациента
def patient_delete(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        logger.info('УДАЛЁН пациент id=%s', patient.id)
        patient.delete()
        messages.success(request, f'Пациент «{patient}» удалён.')
        return redirect('patients:patient_list')
    return render(request, 'patient_confirm_delete.html', {'patient': patient})

# создание осмотра
def osmotr_add(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = OsmotrPatientForm(request.POST)
        if form.is_valid():
            osmotr = form.save(commit=False)
            osmotr.patient = patient
            on_date = form.cleaned_data['on_date']
            osmotr.data_osmotra = timezone.make_aware(
                datetime.combine(on_date, timezone.now().time())
            )
            osmotr.save()
            logger.info('Осмотр добавлен id=%s для patient_id=%s', osmotr.id, patient.id)
            messages.success(request, 'Осмотр добавлен.')
            return redirect('patients:patient_detail', patient_id=patient.pk)
    else:
        form = OsmotrPatientForm()
    return render(request, 'osmotr_form.html', {'form': form, 'patient': patient})

# редактирование осмотра
def osmotr_edit(request, osmotr_id):
    osmotr = get_object_or_404(OsmotrPatient, id=osmotr_id)
    patient = osmotr.patient
    if request.method == 'POST':
        form = OsmotrPatientForm(request.POST, instance=osmotr)
        if form.is_valid():
            osmotr = form.save(commit=False)
            on_date = form.cleaned_data.get('on_date') or timezone.localdate()
            osmotr.data_osmotra = on_date
            osmotr.save()
            logger.info('Осмотр отредактирован id=%s для patient_id=%s', osmotr.id, patient.id)
            messages.success(request, 'Осмотр обновлён.')
            return redirect('patients:patient_detail', patient_id=patient.pk)
    else:
        form = OsmotrPatientForm(instance=osmotr)
    return render(request, 'osmotr_form.html', {'form': form, 'osmotr': osmotr, 'patient': patient})

# удаление осмотра
def osmotr_delete(request, osmotr_id):
    osmotr = get_object_or_404(OsmotrPatient, id=osmotr_id)
    patient_id = osmotr.patient.id
    if request.method == 'POST':
        osmotr.delete()
        logger.info('Удалён осмотр id=%s для patient_id=%s', osmotr.id, patient_id)
        messages.success(request, 'Осмотр удалён.')
    return redirect('patients:patient_detail', patient_id=patient_id)
