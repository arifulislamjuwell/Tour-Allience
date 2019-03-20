from django.shortcuts import render


def home(request):
    templates= 'home.html'
    return render(request,templates)
