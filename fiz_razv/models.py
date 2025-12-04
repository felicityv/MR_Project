from django.db import models
from datetime import date

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
    def save(self):
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


# class FizicRazvit(models.Model):
#     FIZIVRAZ_CHOICES = {
#         "Физическое развитие высокое, гармоничное":"Физическое развитие высокое, гармоничное",
#         "Физическое развитие высокое, дисгармоничное":"Физическое развитие высокое, дисгармоничное",
#         "Физическое развитие высокое, резко дисгармоничное":"Физическое развитие высокое, резко дисгармоничное",
#         "Физическое развитие выше среднего, гармоничное":"Физическое развитие выше среднего, гармоничное",
#         "Физическое развитие выше среднего, дисгармоничное":"Физическое развитие выше среднего, дисгармоничное",
#         "Физическое развитие ниже среднего, гармоничное":"Физическое развитие ниже среднего, гармоничное",
#         "Физическое развитие ниже среднего, дисгармоничное":"Физическое развитие ниже среднего, дисгармоничное",
#         "Физическое развитие низкое, гармоничное":"Физическое развитие низкое, гармоничное",
#         "Физическое развитие низкое, дисгармоничное":"Физическое развитие низкое, дисгармоничное",
#         "Физическое развитие низкое, резко гармоничное":"Физическое развитие низкое, резко гармоничное",
#         "Физическое развитие очень высокое, гармоничное":"Физическое развитие очень высокое, гармоничное",
#         "Физическое развитие очень высокое, дисгармоничное":"Физическое развитие очень высокое, дисгармоничное",
#         "Физическое развитие очень низкое, гармоничное":"Физическое развитие очень низкое, гармоничное",
#         "Физическое развитие очень низкое, дисгармоничное":"Физическое развитие очень низкое, дисгармоничное",
#         "Физическое развитие очень низкое, резко гармоничное":"Физическое развитие очень низкое, резко гармоничное",
#         "Физическое развитие резко дисгармоничное":"Физическое развитие резко дисгармоничное",
#         "Физическое развитие среднее, гармоничное":"Физическое развитие среднее, гармоничное",
#     }
#     type_razvitya = models.CharField(max_length=100, choices=FIZIVRAZ_CHOICES)

class FizicRazvit(models.Model):
    STEPEN_CHOICES = {
        "высокое":"Физическое развитие высокое",
        "выше среднего":"Физическое развитие выше среднего",
        "ниже среднего":"Физическое развитие ниже среднего",
        "низкое":"Физическое развитие низкое",
        "очень высокое":"Физическое развитие очень высокое",
        "очень низкое":"Физическое развитие очень низкое",
        "без определенного вариант":"Физическое развитие без определенного вариант",
        "среднее":"Физическое развитие среднее",
    }
    GARMON_CHOICES = {
        "гарм":"гармоничное",
        "дисгарм":"дисгармоничное",
        "резкодис":"резко дисгармоничное",
    }
    type_razvitya = models.CharField(max_length=100, choices=STEPEN_CHOICES)
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
    rost_centil = models.CharField(max_length=10, choices=CENTIL_CHOICES)
    rost_SDS = models.FloatField()
    ves_сentil = models.CharField(max_length=10, choices=CENTIL_CHOICES)
    ves_SDS = models.FloatField()
    imt_сentil = models.CharField(max_length=10, choices=CENTIL_CHOICES)
    imt_SDS = models.FloatField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fizic_razvitie = models.ManyToManyField(FizicRazvit)
    narushenie = models.ManyToManyField(Narushenie)
    def __str__(self):
        return f'Осмотр {self.patient} от {self.data_osmotra.date()}'


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



