from django.db import models
from datetime import date
from fiz_razv.services import analyze_centile, fizrazvitie
from fiz_razv.models import Narushenie
from fiz_razv.models import Rost, Ves, Imt

class Patient(models.Model):
    GENDER_CHOICES = {
        "М": "Мужской",
        "Ж": "Женский"
    }
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    data_birth = models.DateField()
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    rost = models.FloatField()
    ves = models.FloatField()
    imt = models.FloatField(editable=False)
    foto = models.ImageField(upload_to="photos/", height_field="height", width_field="width", null=True, blank=True)
    height = models.IntegerField(null=True, blank=True, editable=False)
    width = models.IntegerField(null=True, blank=True, editable=False)

    def __str__(self):
        return f'{self.surname} {self.name}'
    
    def save(self,*args, **kwargs):
        self.imt = round(self.ves / ((self.rost / 100) ** 2), 1)
        super().save(*args, **kwargs)

    @property
    def calculate_age(self) -> tuple[int, int]:
        today = date.today()
        years =today.year - self.data_birth.year
        months = today.month - self.data_birth.month
        days = today.day - self.data_birth.day
        if days < 0:
            months -= 1
        if months < 0:
            years -= 1
            months += 12
        return years, months
    
    @property
    def age_display(self):
        years, months = self.calculate_age
        return f"{years} лет {months} месяцев"

class OsmotrPatient(models.Model):
    CENTIL_CHOICES = {
        "ниже 3": "ниже 3",
        "3-10": "3-10",
        "10-25": "10-25",
        "25-75": "25-75",
        "75-90": "75-90",
        "90-97": "90-97",
        "выше 97": "выше 97"
    }
    data_osmotra = models.DateTimeField(auto_now_add=True)
    rost = models.FloatField()
    ves = models.FloatField()
    imt = models.FloatField(editable=False)
    rost_centil = models.CharField(max_length=10, choices=CENTIL_CHOICES, editable=False)
    rost_SDS = models.FloatField(editable=False)
    ves_centil = models.CharField(max_length=10, choices=CENTIL_CHOICES, editable=False)
    ves_SDS = models.FloatField(editable=False)
    imt_centil = models.CharField(max_length=10, choices=CENTIL_CHOICES, editable=False)
    imt_SDS = models.FloatField(editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fizic_razvitie = models.ManyToManyField("fiz_razv.FizicRazvit", editable=False)
    narushenie = models.ManyToManyField("fiz_razv.Narushenie", editable=False)

    def save(self, *args, **kwargs):
        self.imt = round(self.ves / ((self.rost / 100) ** 2), 1)
        age_years = self.patient.calculate_age[0]
        gender = self.patient.gender
        self.rost_SDS, self.rost_centil = analyze_centile(self.patient.rost, Rost, age_years, gender)
        self.ves_SDS, self.ves_centil = analyze_centile(self.patient.ves, Ves, age_years, gender)
        self.imt_SDS, self.imt_centil = analyze_centile(self.patient.imt, Imt, age_years, gender)
        fiz_text = fizrazvitie(self.rost_centil, self.ves_centil)
        print(fiz_text)
        self.patient.rost = self.rost
        self.patient.ves = self.ves
        self.patient.imt = self.imt
        self.patient.save(update_fields=["rost", "ves", "imt"])
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Осмотр {self.patient} от {self.data_osmotra.date()}'



