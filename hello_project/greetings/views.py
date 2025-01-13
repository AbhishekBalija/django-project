from django.http import HttpResponse
from django.shortcuts import render;

def say_hello(request):
    return HttpResponse("Hello from Django!")

def index(request):
    return render(request, 'greeting/index.html')