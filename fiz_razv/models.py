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
    def __str__(self):
        return f'{self.surname} {self.name}'

class Har_Pokaz(models.Model):
    GENDER_CHOICES = {
        "М": "Мужской",
        "Ж": "Женский"
    }
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    age = models.FloatField()
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



