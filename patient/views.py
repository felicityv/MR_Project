from django.shortcuts import render
from django.http import HttpRequest

def main(request):
    return HttpResponse("Привет МИР!")


