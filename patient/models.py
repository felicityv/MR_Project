from django.db import models
from django.utils import timezone
from mkb10.models import MKB10
from fiz_razv.models import Rost, Ves, Imt

class Patient(models.Model):
    GENDER_CHOICES = [("М", "Мужской"), ("Ж", "Женский")]

    surname = models.CharField(max_length=100, db_index=True)
    name    = models.CharField(max_length=100, db_index=True)
    data_birth = models.DateField(db_index=True)
    gender  = models.CharField(max_length=1, choices=GENDER_CHOICES, db_index=True)
    mkb = models.ForeignKey(MKB10, on_delete=models.PROTECT, null=True, blank=True)
    diagnoz_osn = models.CharField(max_length=1000, null=True, blank=True)
    diagnoz_sop = models.CharField(max_length=1000, null=True, blank=True)
    suz = models.IntegerField(null=True, blank=True)

    # кэш-поля (обновляются при сохранении последнего осмотра)
    rost = models.FloatField(null=True, blank=True)
    ves  = models.FloatField(null=True, blank=True)
    imt  = models.FloatField(null=True, blank=True, editable=False)

    foto   = models.ImageField(
        upload_to="photos/%Y/%m/", height_field="height",
        width_field="width", null=True, blank=True
    )
    height = models.IntegerField(null=True, blank=True, editable=False)
    width  = models.IntegerField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["surname", "name"]

    def __str__(self):
        return f"{self.surname} {self.name}"

    def save(self, *args, **kwargs):
        if self.rost and self.ves:
            self.imt = round(self.ves / ((self.rost / 100) ** 2), 1)
        super().save(*args, **kwargs)

    @property
    def calculate_age(self) -> tuple[int, int]:
        today = timezone.now().date()
        years = today.year - self.data_birth.year
        months = today.month - self.data_birth.month
        if today.day < self.data_birth.day:
            months -= 1
        if months < 0:
            years -= 1
            months += 12
        return years, months

    @property
    def age_display(self):
        y, m = self.calculate_age
        return f"{y} лет {m} месяцев"

from django.db import transaction
from fiz_razv.services import analyze_centile, fizrazvitie, calculate_age_key, narushenia

class OsmotrPatient(models.Model):
    POTENCIAL_CHOICES = [
        ("В", "высокий"), ("С", "средний"), ("Н", "низкий"),
        ("КН", "крайне низкий"), ("О", "отсутствует"),
    ]
    CENTIL_CHOICES = [
        ("ниже 3", "ниже 3"), ("3-10", "3-10"), ("10-25", "10-25"),
        ("25-75", "25-75"), ("75-90", "75-90"),
        ("90-97", "90-97"), ("выше 97", "выше 97"),
    ]

    data_osmotra = models.DateField(default=timezone.localdate)
    diagnoz_osn  = models.CharField(max_length=1000, null=True, blank=True)
    diagnoz_sop  = models.CharField(max_length=1000, null=True, blank=True)
    suz = models.IntegerField(null=True, blank=True)
    rp  = models.CharField(max_length=15, choices=POTENCIAL_CHOICES, null=True, blank=True)

    rost = models.FloatField(null=True, blank=True)
    ves  = models.FloatField(null=True, blank=True)
    imt  = models.FloatField(editable=False, null=True, blank=True)

    rost_centil = models.CharField(max_length=10, choices=CENTIL_CHOICES, editable=False, null=True, blank=True)
    rost_SDS    = models.FloatField(editable=False, null=True, blank=True)
    ves_centil  = models.CharField(max_length=10, choices=CENTIL_CHOICES, editable=False, null=True, blank=True)
    ves_SDS     = models.FloatField(editable=False, null=True, blank=True)
    imt_centil  = models.CharField(max_length=10, choices=CENTIL_CHOICES, editable=False, null=True, blank=True)
    imt_SDS     = models.FloatField(editable=False, null=True, blank=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="osmotrs")
    fizic_razvitie = models.ManyToManyField("fiz_razv.FizicRazvit", editable=False)
    narushenie     = models.ManyToManyField("fiz_razv.Narushenie", editable=False)

    class Meta:
        ordering = ["-data_osmotra"]

    def __str__(self):
        return f"Осмотр {self.patient} ({self.data_osmotra})"

    # -------------------- вспомогательное --------------------
    def _age_key(self):
        years, months = self.patient.calculate_age
        return calculate_age_key(years, months)

    # -------------------- основной save --------------------
    @transaction.atomic
    def save(self, *args, **kwargs):
        # 1. ИМТ
        if self.rost and self.ves:
            self.imt = round(self.ves / ((self.rost / 100) ** 2), 1)

        # 2. центили и СДС
        age_key = self._age_key()
        gender  = self.patient.gender

        if self.rost:
            self.rost_SDS, self.rost_centil = analyze_centile(self.rost, Rost, age_key, gender)
        if self.ves:
            self.ves_SDS, self.ves_centil  = analyze_centile(self.ves, Ves, age_key, gender)
        if self.imt:
            self.imt_SDS, self.imt_centil  = analyze_centile(self.imt, Imt, age_key, gender)

        # 3. сохраняем себя
        super().save(*args, **kwargs)

        # 4. many-to-many
        if self.rost_centil and self.ves_centil:
            self.fizic_razvitie.add(fizrazvitie(self.rost_centil, self.ves_centil))

        years, _ = self.patient.calculate_age
        nar_obj, _ = narushenia(self.rost_SDS, self.ves_SDS, self.imt_SDS, years)
        self.narushenie.add(nar_obj)

        # 5. обновляем кэш в Patient
        latest = (self.patient.osmotrs
                  .exclude(pk=self.pk)
                  .order_by('-data_osmotra')
                  .first())
        if not latest or self.data_osmotra > latest.data_osmotra:
            self.patient.rost = self.rost
            self.patient.ves  = self.ves
            self.patient.imt  = self.imt
            self.patient.diagnoz_osn = self.diagnoz_osn
            self.patient.diagnoz_sop = self.diagnoz_sop
            self.patient.suz = self.suz
            self.patient.save()


class PatientImage(models.Model):
    img = models.ImageField(upload_to="patient_image/%Y/%m/")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"Фото {self.patient} ({self.img.name})"

    class Meta:
        ordering = ["-id"]



# from django.db import models
# from datetime import date
# from fiz_razv.models import Rost, Ves, Imt
# from mkb10.models import MKB10
# from django.utils import timezone

# class Patient(models.Model):
#     GENDER_CHOICES = [
#         ("М", "Мужской"),
#         ("Ж", "Женский"),
#     ]
#     surname = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     data_birth = models.DateField()
#     gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
#     kod_mkb = models.ForeignKey(MKB10, on_delete=models.PROTECT, verbose_name='Диагноз по МКБ-10')
#     diagnoz_osn = models.CharField(max_length=1000, null=True, blank=True)
#     diagnoz_sop = models.CharField(max_length=1000, null=True, blank=True)
#     suz = models.IntegerField(null=True, blank=True)
#     rost = models.FloatField()
#     ves = models.FloatField()
#     imt = models.FloatField(editable=False)
#     foto = models.ImageField(upload_to="photos/", height_field="height", width_field="width", null=True, blank=True)
#     height = models.IntegerField(null=True, blank=True, editable=False)
#     width = models.IntegerField(null=True, blank=True, editable=False)

#     def __str__(self):
#         return f'{self.surname} {self.name}'
    
#     def save(self,*args, **kwargs):
#         self.imt = round(self.ves / ((self.rost / 100) ** 2), 1)
#         super().save(*args, **kwargs)

#     @property
#     def calculate_age(self) -> tuple[int, int]:
#         today = date.today()
#         years =today.year - self.data_birth.year
#         months = today.month - self.data_birth.month
#         days = today.day - self.data_birth.day
#         if days < 0:
#             months -= 1
#         if months < 0:
#             years -= 1
#             months += 12
#         return years, months
    
#     @property
#     def age_display(self):
#         years, months = self.calculate_age
#         return f"{years} лет {months} месяцев"
    
# class OsmotrPatient(models.Model):
#     POTENCIAL_CHOICES = [
#         ("В", "высокий"),
#         ("С", "средний"),
#         ("Н", "низкий"),
#         ("КН", "крайне низкий"),
#         ("О", "отсутсвует"),
#         ]
#     CENTIL_CHOICES = [
#         ("ниже 3", "ниже 3"),
#         ("3-10", "3-10"),
#         ("10-25", "10-25"),
#         ("25-75", "25-75"),
#         ("75-90", "75-90"),
#         ("90-97", "90-97"),
#         ("выше 97", "выше 97"),
#         ]
#     data_osmotra = models.DateField(default=timezone.localdate)
#     diagnoz_osn = models.CharField(max_length=1000, null=True, blank=True)
#     diagnoz_sop = models.CharField(max_length=1000, null=True, blank=True)
#     suz = models.IntegerField(null=True, blank=True)
#     rp = models.CharField(max_length=15, choices=POTENCIAL_CHOICES, null=True, blank=True)
#     rost = models.FloatField(null=True, blank=True)
#     ves = models.FloatField(null=True, blank=True)
#     imt = models.FloatField(editable=False, null=True, blank=True)
#     rost_centil = models.CharField(max_length=10, choices=CENTIL_CHOICES, editable=False, null=True, blank=True)
#     rost_SDS = models.FloatField(editable=False, null=True, blank=True)
#     ves_centil = models.CharField(max_length=10, choices=CENTIL_CHOICES, editable=False, null=True, blank=True)
#     ves_SDS = models.FloatField(editable=False, null=True, blank=True)
#     imt_centil = models.CharField(max_length=10, choices=CENTIL_CHOICES, editable=False, null=True, blank=True)
#     imt_SDS = models.FloatField(editable=False, null=True, blank=True)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     fizic_razvitie = models.ManyToManyField("fiz_razv.FizicRazvit", editable=False)
#     narushenie = models.ManyToManyField("fiz_razv.Narushenie", editable=False)

#     def save(self, *args, **kwargs):
#         from fiz_razv.services import (
#             analyze_centile, fizrazvitie, calculate_age_key, narushenia
#         )
#         self.imt = round(self.ves / ((self.rost / 100) ** 2), 1)
#         on_date = self.data_osmotra
#         years = on_date.year - self.patient.data_birth.year
#         months = on_date.month - self.patient.data_birth.month
#         days = on_date.day - self.patient.data_birth.day
#         if days < 0:
#             months -= 1
#         if months < 0:
#             years -= 1
#             months += 12
#         age_key = calculate_age_key(years, months)
#         gender = self.patient.gender
#         self.rost_SDS, self.rost_centil = analyze_centile(
#             self.rost, Rost, age_key, gender)
#         self.ves_SDS, self.ves_centil = analyze_centile(
#             self.ves, Ves, age_key, gender)
#         self.imt_SDS, self.imt_centil = analyze_centile(
#             self.imt, Imt, age_key, gender)

#         super().save(*args, **kwargs)

#         fiz_obj = fizrazvitie(self.rost_centil, self.ves_centil)
#         self.fizic_razvitie.add(fiz_obj)
#         nar_obj, _ = narushenia(
#             self.rost_SDS, self.ves_SDS, self.imt_SDS, years)
#         self.narushenie.add(nar_obj)
#         latest = (
#             self.patient.osmotrpatient_set
#                .exclude(pk=self.pk)
#                .first()
# )
#         if not latest or self.data_osmotra > latest.data_osmotra:
#             self.patient.rost = self.rost
#             self.patient.ves = self.ves
#             self.patient.imt = self.imt
#             self.patient.diagnoz_osn = self.diagnoz_osn
#             self.patient.diagnoz_sop = self.diagnoz_sop
#             self.patient.suz = self.suz
#             self.patient.rp = self.rp
#             self.patient.save()

#     @property
#     def age_on_date_display(self):
#         on_date = self.data_osmotra
#         years = on_date.year - self.patient.data_birth.year
#         months = on_date.month - self.patient.data_birth.month
#         days = on_date.day - self.patient.data_birth.day
#         if days < 0:
#             months -= 1
#         if months < 0:
#             years -= 1
#             months += 12
#         return f"{years} лет {months} месяцев"

# class PatientImage(models.Model):
#     img=models.ImageField(upload_to='patient_image')
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

