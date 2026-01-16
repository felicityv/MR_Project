from django.db import models

class LoginFormM(models.Model):
    """Модель для формы входа (логин + пароль)"""
    login    = models.CharField(max_length=100, db_index=True)
    passward = models.CharField(max_length=100, db_index=True)  # опечатка сохранена

    def __str__(self):
        return self.login


class RegisterFormM(models.Model):
    """Модель для формы регистрации (с фото)"""
    email     = models.EmailField(unique=True)
    login     = models.CharField(max_length=100, unique=True, db_index=True)
    passward1 = models.CharField(max_length=100,)
    passward2 = models.CharField(max_length=100)
    foto      = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True,
        null=True,
        help_text='Необязательно. JPG/PNG, max 2 МБ'
    )


    def __str__(self):
        return self.login