from django.shortcuts import render
from django.http import HttpRequest
from .models import Author

# def form_view(request):
#     return render(request, 'my_form.html')

def get_form(request):
    # authors = Author.objects.all()
    authors = Author.objects.all().order_by("-id")
    last_author=authors[0]
    print(authors[])
    context = {
        "authors":authors,
        "errors":[],
        "last_author":last_author
    }
    if request.method == "POST":
        # print(request.POST)
        # if len(request.POST.get("age"))> 0 and len(request.POST.get("first_name"))> 0 and len(request.POST.get("last_name"))> 0:
        #     new_author = Author.objects.create(first_name=request.POST.get("first_name"), last_name=request.POST.get("last_name"), age=request.POST.get("age"))
        # else:
        #     print("НЕТ ДАННЫХ")
        age=request.POST.get("age")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        if len(age)> 0 and len(first_name)> 0 and len(last_name)> 0:
            if age.isdigit():
                new_author = Author(first_name=first_name, last_name=last_name, age=age)
                new_author.save
            else:
                context.get("errors").append("Возраст должен быть числом")
                print("Возраст должен быть числом")
        else:
            context.get("errors").append("Все должно быть заполнено")
            print("Все должно быть заполнено")

    return render(request, 'my_form.html', context)