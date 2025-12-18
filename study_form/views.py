from django.shortcuts import render
from django.http import HttpRequest
from .models import Author

# def form_view(request):
#     return render(request, 'my_form.html')

def get_form(request):
    authors = Author.objects.all()
    if request.method == "POST":
        print(request.POST)
        if len(request.POST.get("age"))> 0 and len(request.POST.get("first_name"))> 0 and len(request.POST.get("last_name"))> 0:
            new_author = Author.objects.create(first_name=request.POST.get("first_name"), last_name=request.POST.get("last_name"), age=request.POST.get("age"))
        else:
            print("НЕТ ДАННЫХ")
    context = {
        "authors":authors
    }
    return render(request, 'my_form.html', context)