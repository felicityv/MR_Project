from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegisterFormF, LoginFormF
from .models import RegisterFormM 

#главная
def main(request):
    return render(request, 'main.html')

#регистрация
def register(request):
    if request.method == 'POST':
        form = RegisterFormF(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id)
            form.save()
            messages.success(request, 'Регистрация завершена')
            return redirect('login')
    else:
        form = RegisterFormF()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginFormF(request.POST)
        if form.is_valid():
            login    = form.cleaned_data['login']
            password = form.cleaned_data['passward']
            try:
                user = RegisterFormM.objects.get(login=login)
                if check_password(password, user.passward1):
                    request.session['user_id'] = user.id
                    return redirect('profile')
                else:
                    form.add_error(None, 'Неверный логин или пароль')
            except RegisterFormM.DoesNotExist:
                form.add_error(None, 'Неверный логин или пароль')
    else:
        form = LoginFormF()
    return render(request, 'loginpage.html', {'form': form})

#личный кабинет
def profile(request):
    uid = request.session.get('user_id')
    if not uid:
        return redirect('login')
    user = RegisterFormM.objects.get(pk=uid)
    return render(request, 'profile.html', {'user': user})

#выход
def user_logout(request):
    request.session.flush()
    return redirect('login')