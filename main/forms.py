from django import forms
from django.forms import ModelForm
from django.contrib.auth.password_validation import validate_password
from .models import LoginFormM, RegisterFormM


class LoginFormF(ModelForm):
    """Форма входа"""
    class Meta:
        model = LoginFormM
        fields = ['login', 'passward']
        widgets = {
            'passward': forms.PasswordInput(),
        }


class RegisterFormF(ModelForm):
    """Форма регистрации с валидацией пароля и фото"""
    class Meta:
        model = RegisterFormM
        fields = ['email', 'login', 'passward1', 'passward2', 'foto']
        widgets = {
            'passward1': forms.PasswordInput(),
            'passward2': forms.PasswordInput(),
        }

    # ---------- валидация файла ----------
    def clean_foto(self):
        foto = self.cleaned_data['foto']
        if not foto:
            return foto
        if foto.size > 2 * 1024 * 1024:          # 2 МБ
            raise forms.ValidationError('Файл больше 2 МБ')
        ext = foto.name.split('.')[-1].lower()
        if ext not in ('jpg', 'jpeg', 'png'):
            raise forms.ValidationError('Разрешены JPG, JPEG, PNG')
        return foto

    # ---------- валидация пароля ----------
    def clean_passward1(self):
        pw = self.cleaned_data.get('passward1')
        if pw:
            validate_password(pw)
        return pw

    # ---------- совпадение паролей ----------
    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('passward1')
        pw2 = cleaned.get('passward2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned