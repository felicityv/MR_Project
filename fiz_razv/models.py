from django.db import models

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
    imt = models.FloatField()
    foto = models.ImageField(upload_to="photos/", height_field="height", width_field="width", null=True, blank=True)
    height = models.IntegerField(null=True, blank=True, editable=False)
    width = models.IntegerField(null=True, blank=True, editable=False)
    def __str__(self):
        return f'{self.surname} {self.name}'

class Narushenie(models.Model):
    type_narushenia = models.CharField(max_length=100)

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
    FIZIC_CHOICES = {
        "ниже 3": "ниже 3",
        "3-10": "3-10",
        "10-25": "10-25",
        "25-75": "25-75",
        "75-90": "75-90",
        "90-97": "90-97",
        "выше 97": "выше 97"
    }
    data_osmotra = models.DateTimeField(auto_now_add=True)
    rost_сentil = models.CharField(max_length=10, choices=CENTIL_CHOICES)
    rost_SDS = models.FloatField()
    ves_сentil = models.CharField(max_length=10, choices=CENTIL_CHOICES)
    ves_SDS = models.FloatField()
    imt_сentil = models.CharField(max_length=10, choices=CENTIL_CHOICES)
    ves_SDS = models.FloatField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fizic_razvitie = models.CharField(max_length=100, choices=FIZIC_CHOICES)
    narushenie = models.ManyToManyField(Narushenie)




class Har_Pokaz(models.Model):
    GENDER_CHOICES = {
        "М": "Мужской",
        "Ж": "Женский"
    }
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    age = models.FloatField()
    # age_int1 = models.FloatField(null=True, blank=True)
    # age_int2 = models.FloatField(null=True, blank=True)
    ME = models.FloatField()
    SD = models.FloatField()
    p3 = models.FloatField()
    p10 = models.FloatField()
    p25 = models.FloatField()
    p50 = models.FloatField()
    p75 = models.FloatField()
    p90 = models.FloatField()
    p97 = models.FloatField()

    class Meta:
        abstract=True  #позволяет не создавать таблицу в базе данных
    
    def __str__(self):
        return f'{self.gender} {self.age}'

class Rost(Har_Pokaz):
    pass

class Ves(Har_Pokaz):
    pass

class Imt(Har_Pokaz):
    pass



