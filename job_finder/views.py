from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world! This is the blog app.")

def index(request):
    return render(request,'index.html')

def first(request):
    return render(request,'first.html')
