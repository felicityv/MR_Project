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


# class Anthro_Pokaz(models.Model):
#     pokazatel = models.CharField(max_length=10)
#     izmerenie = models.CharField(max_length=10)

#     def __str__(self):
#         return f'{self.pokazatel}'
    
# class Percentile(models.Model):



#     def __str__(self):
#         return f'{self.pokazatel}'