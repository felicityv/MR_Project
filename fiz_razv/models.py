from django.db import models
from datetime import date
from .services import analyze_centile, fizrazvitie

class FizicRazvit(models.Model):
    STEPEN_CHOICES = {
        "В":"высокое",
        "ВС":"выше среднего",
        "НС":"ниже среднего",
        "Н":"низкое",
        "ОВ":"очень высокое",
        "ОН":"очень низкое",
        "БОВ":"без определенного вариант",
        "С":"среднее",
    }
    GARMON_CHOICES = {
        "Г":"гармоничное",
        "ДГ":"дисгармоничное",
        "РДГ":"резко дисгармоничное",
    }
    type_razvitya = models.CharField(max_length=30, choices=STEPEN_CHOICES)
    type_garmonic = models.CharField(max_length=30, choices=GARMON_CHOICES)
    def __str__(self):
        return f'{self.type_razvitya}, {self.type_garmonic}'

class Narushenie(models.Model):
    NARUSH_CHOICES = {
        "ХБЭН": "Низкорослость или хроническая белково-энергетическая недостаточность, умеренной степени",
        "Выс": "Высокорослость",
        "Ожир": "Ожирение",
        "ИМТ": "Избыток массы тела",
        "ОБЭН3": "Острая белково-энергетическая недостаточность, тяжёлой степени",
        "ОБЭН2": "Острая белково-энергетическая недостаточность, умеренной степени",
        "Нарушений не выявлено": "Нарушений не выявлено"
    }
    type_narushenia = models.CharField(max_length=100, choices=NARUSH_CHOICES)
    def __str__(self):
        return self.type_narushenia

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



