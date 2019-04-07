from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.db.models import F
import facebook
# Create your views here.

def index(request):
    templates= 'index.html'
    alltour=Tour.objects.all().order_by('-pk')
    usertour=Tour.objects.filter(creator=request.user)
    context={'alltour':alltour,'usertour':usertour}
    if request.method=='POST':
        tour= Tour()
        tour.creator=request.user
        title=tour.title=request.POST.get('title')
        tour.location=request.POST.get('location')
        tour.duration=request.POST.get('duration')
        date=tour.date_of_tour=request.POST.get('date')
        tour.fee =request.POST.get('fee')
        tour.short_description= request.POST.get('description')
        tour.save()
        token='EAAFdmc17CgkBAGGSUJKblohZA9wizjLl4dZA6rGsuRT8Ma21UZCUHS06EuB69aqqR1nYoZAVZAhMEju9e4GwP68NF1GYYlZAfAtXjzUmZCRcCqjFWy2sMeZCGuKgA2uPGCu5BxkRSVq0hw4ehJJaOCZB33mqc60pm9aBOlXlbwupAi7qFZBuAZAtjlP1ggEg1Czi2byh656gqGKVH87mZCc5gdsl'
        fb=facebook.GraphAPI(access_token=token)
        fb.put_object(parent_object='me',connection_name='feed',message='welcome!a new tour arrive.Tour name:'+str(title)+'Date:'+str(date))
        return redirect('index')

    return render(request,templates,context)

def joining(request,pk):
    tour = get_object_or_404(Tour,pk=pk)
    fee=int(tour.fee)
    try:
        check=get_object_or_404(Finance_Board, tour=tour)
    except:
        obj_finance=Finance_Board()
        obj_finance.tour=tour
        obj_finance.save()
    Finance_Board.objects.all().filter(tour=tour).update(total_expeted=F('total_expeted')+fee,due=F('due')+fee)

    userobj= get_object_or_404(User, username= request.user)
    username=userobj.username
    mail=userobj.email

    member=Member_on_tour()
    member.tour=tour
    member.name=username
    member.mail=mail
    member.paid_money=0
    member.due=fee
    member.save()
    return redirect('index')

def all_tour_details(request,slug):
    templates= 'tourrelated/all_tour_details.html'
    tour=get_object_or_404(Tour, slug=slug)
    check= Member_on_tour.objects.all().filter(tour=tour, name=request.user)
    context= {'tour':tour,'check':check}
    return render(request,templates,context)

def my_tour_details(request,slug):
    templates= 'tourrelated/my_tour_details.html'
    tour=get_object_or_404(Tour, slug=slug)
    allmember=Member_on_tour.objects.all().filter(tour=tour)
    try:
        check=get_object_or_404(Finance_Board, tour=tour)
    except:
        obj_finance=Finance_Board()
        obj_finance.tour=tour
        obj_finance.save()
    account=get_object_or_404(Finance_Board, tour=tour)
    context={'member':allmember,'tour':tour,'acc':account}
    return render(request,templates,context)

def add_member(request,pk):
    tour=get_object_or_404(Tour, pk=pk)
    fee=int(tour.fee)
    if request.method == "POST":
        memberobj= Member_on_tour()
        memberobj.tour=tour
        memberobj.name=request.POST.get('name')
        memberobj.mail=request.POST.get('email')
        memberobj.p_money=request.POST.get('give')
        memberobj.due=request.POST.get('due')
        memberobj.save()
        try:
            check=get_object_or_404(Finance_Board, tour=tour)
        except:
            obj_finance=Finance_Board()
            obj_finance.tour=tour
            obj_finance.save()
        Finance_Board.objects.all().filter(tour=tour).update(total_expeted=F('total_expeted')+fee,Current_money=F('Current_money')+int(request.POST.get('give')),due=F('due')+int(request.POST.get('due')))
        return redirect('my_tour_details', slug=tour.slug )

def expense(request,pk):
    tour=get_object_or_404(Tour, pk=pk)
    if request.method == "POST":
        expenseobj= Expense()
        expenseobj.tour=tour
        expenseobj.title=request.POST.get('title')
        expenseobj.description=request.POST.get('descrip')
        expenseobj.ammount=request.POST.get('ammount')
        expenseobj.save()
        try:
            check=get_object_or_404(Finance_Board, tour=tour)
        except:
            obj_finance=Finance_Board()
            obj_finance.tour=tour
            obj_finance.save()
        Finance_Board.objects.all().filter(tour=tour).update(expens=F('expens')+int(request.POST.get('ammount')),Current_money=F('Current_money')-int(request.POST.get('ammount')))
        return redirect('my_tour_details', slug=tour.slug )

def schedule(request,pk):
    tour=get_object_or_404(Tour, pk=pk)
    if request.method == "POST":
        scobj= Schedule()
        scobj.tour=tour
        scobj.day=request.POST.get('day')
        scobj.time=request.POST.get('time')
        scobj.task=request.POST.get('task')
        scobj.save()
        return redirect('my_tour_details', slug=tour.slug )
