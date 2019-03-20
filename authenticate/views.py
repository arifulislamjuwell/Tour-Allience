from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def registration(request):
    templates ='auth/registration.html'
    contex_password= {'error_pass':'password doesn\'t match'}
    contex_user= {'user_error':'This Username Alredy Taken'}

    if request.method == "POST":
        if request.POST['password1']== request.POST['password2']:
            try:
                users= User.objects.get(username=request.POST['username'])
                if users:
                    return render(request,templates,contex_user)
            except User.DoesNotExist:
                users= User.objects.create_user(request.POST['username'], password=request.POST['password1'],email=request.POST['email'])
                auth.login(request, users)
                return redirect('index')

        else:
            return render(request,templates,contex_password)
    else:
        return render(request,templates)



def login (request):
    contex_error={'error_user':'Username Or Password Is Incorrect'}
    templates= 'auth/login.html'

    if request.method=="POST":
        user =auth.authenticate(username= request.POST['username'], password= request.POST['password1'])
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request,templates,contex_error)
    else:
        return render(request,templates)

@login_required
def logout (request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('home')
