from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Funcia(models.Model):
    code = models.CharField("код", max_length=20, unique=True)
    name = models.CharField("название", max_length=100)

    class Meta:
        verbose_name = "категория функций"
        verbose_name_plural = "категории функций"
        ordering = ["code"]

    def __str__(self):
        return self.name


class FunciaVid(models.Model):
    category = models.ForeignKey(
        Funcia,
        on_delete=models.CASCADE,
        related_name="вид",
        verbose_name="категория",
    )
    code = models.CharField("код", max_length=20)
    name = models.CharField("название", max_length=150)

    class Meta:
        unique_together = ("category", "code")
        verbose_name = "вид функции"
        verbose_name_plural = "виды функций"
        ordering = ["category", "code"]

    def __str__(self):
        return f"{self.category.name} – {self.name}"


class StepenFuncii(models.Model):
    stenen = models.PositiveSmallIntegerField(
        "степень выраженности нарушения",
        unique=True,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        help_text="0 = нарушение отсутствует, 6 = полное нарушение",
    )
    title = models.CharField("название", max_length=30)

    class Meta:
        verbose_name = "степень выраженности нарушения"
        verbose_name_plural = "степени выраженности нарушений"
        ordering = ["stenen"]

    def __str__(self):
        return self.title


class KriteriiInvalid(models.Model):
    fio = models.CharField("Ф.И.О.", max_length=100)
    birth_date = models.DateField("дата рождения", blank=True, null=True)
    created_at = models.DateTimeField("создано", auto_now_add=True)

    class Meta:
        verbose_name = "критерий инвалидности"
        verbose_name_plural = "критерии инвалидности"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Карточка {self.fio}"


class FuncStatus(models.Model):
    """Связь «пациент – функция – степень»."""
    patient = models.ForeignKey(
        KriteriiInvalid,
        on_delete=models.CASCADE,
        related_name="statuses",
        verbose_name="пациент",
    )
    func = models.ForeignKey(
        StepenFuncii,
        on_delete=models.PROTECT,
        related_name="func_statuses",
        verbose_name="функция",
    )
    severity = models.ForeignKey(
        StepenFuncii,
        on_delete=models.PROTECT,
        related_name="severity_statuses",
        verbose_name="степень",
    )

    class Meta:
        unique_together = ("patient", "func")
        verbose_name = "статус функции"
        verbose_name_plural = "статусы функций"

    def __str__(self):
        return f"{self.patient.fio}: {self.func} – {self.severity}"






# class KriteriiInvalid(models.Model):
#     OGRANICHENIA_CHOICES = [
#         ("сам", "способность к самообслуживанию"),
#         ("пер", "способность к самостоятельному передвижению"),
#         ("ориен", "способность к ориентации"),
#         ("общ", "способность к общению"),
#         ("конт", "способность контролировать свое поведение"),
#         ("обуч", "способность к обучению"),
#         ("труд", "способность к трудовой деятельности (выполнению трудовой функции)"),
#         ("вед", "способность к ведущей возрастной деятельности"),
#     ]

#     FUNCII_CHOICES = [
#         ("псих", "нарушения психических функций"),
#         ("гол", "нарушения функций голоса и речи"),
#         ("сенс", "нарушения сенсорных функций"),
#         ("статодин", "нарушения статодинамической функции"),
#         ("хват", "нарушение функции хвата и удержания кисти"),
#         ("ман", "нарушение манипуляционной функции кисти"),        
#         ("кровообр", "нарушения функций кровообращения"),
#         ("дых", "нарушения функций дыхания"),
#         ("пищ", "нарушения функций пищеварения"),
#         ("РДГ", "нарушения функций выделения"),
#         ("кроветв", "нарушения функций кроветворения"),
#         ("обмен", "нарушения функций обмена веществ и метаболизма"),
#         ("секр", "нарушения функций внутренней и внешней (потоотделения) секреции"),
#     ]
#     FUNCIIGOLOSA_CHOICES = [
#         ("реч", "речевого развития"),
#         ("уст", "устной речи (ринолалия, дизартрия, заикание, тахилалия, брадилалия)"),
#         ("писм", "письменной речи (дисграфия, дислексия)"),
#         ("умс", "умственных функции речи (алалия, афазия)"),
#     ]
#     FUNCIISENSORNIE_CHOICES = [
#         ("зр", "зрения"),
#         ("сл", "слуха"),
#         ("обон", "обоняния"),
#         ("осяз", "осязания"),
#         ("такт", "тактильной чувтвительности"),
#         ("болев", "болевой чувтвительности"),
#         ("темп", "температурной чувтвительности"),
#         ("вибр", "вибрационной чувтвительности"),
#         ("бол", "боли"),
#     ]

#     FUNCIISTANODIN_CHOICES = [
#         ("гол", "движения головы"),
#         ("тул", "движения туловища"),
#         ("кон", "движения конечностей"),
#         ("опор", "опоры и ходьбы"),
#         ("стат", "статики"),
#         ("коорд", "координации движений"),
#         ("вест", "вестибулярной функции"),
#     ]
#  (речевого развития (у лиц в возрасте 18 лет и старше); устной речи (ринолалия, дизартрия, заикание, тахилалия, брадилалия), письменной речи (дисграфия, дислексия), голосообразования), умственных функции речи (алалия, афазия)








# (в ред. постановления Минздрава от 16.09.2025 N 109)

# (см. текст в предыдущей редакции)

# 1.13

# нарушения функций иммунитета

# 1.14

# нарушения функций приема нутриентов (кусания, жевания, глотания, сосания (у лиц в возрасте до 1 года)

# (пп. 1.14 введен постановлением Минздрава от 16.09.2025 N 109)

# 1.15

# нарушения функций синтеза соединительной ткани


#     ]
#     type_razvitya = models.CharField(max_length=30, choices=STEPEN_CHOICES)
#     type_garmonic = models.CharField(max_length=30, choices=GARMON_CHOICES)
#     def get_type_razvitya_display(self):
#         return dict(self.STEPEN_CHOICES).get(self.type_razvitya, self.type_razvitya)
#     def get_type_garmonic_display(self):
#         return dict(self.GARMON_CHOICES).get(self.type_garmonic, self.type_garmonic)
#     def __str__(self):
#         return f'{self.get_type_razvitya_display()}, {self.get_type_garmonic_display()}'

