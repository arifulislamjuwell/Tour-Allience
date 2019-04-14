from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.db.models import F
import facebook
# Create your views here.

def cratetour(request):
    templates='create.html'

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
        token='EAAFdmc17CgkBAOZAnnZBY6ypXqySL32IhuPzvZBjHjhGcJC9XDzF3aPR8JiZBjbMI9fAGdZCfvwgG73Dp7xTQ49KKadElVxmfj3YUV0xzz40YvYAvqhYDBb4DkkKk2k263GJnOFZBZAIOeLEJ3OAcogiEl9907lZBZADCcxYIPn4ECKOo0gTWDiZA9gg8HWyrlWN064hwJQy4vxZCIhATDhgEev'
        fb=facebook.GraphAPI(access_token=token)
        fb.put_object(parent_object='me',connection_name='feed',message='welcome!a new Tour Arrived.'+'Tour name:'+str(title)+'Date:'+str(date))
        return redirect('home')

    return render(request,templates)

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
    return redirect('home')

def all_tour_details(request,slug):
    templates= 'tourrelated/all_tour_details.html'
    tour=get_object_or_404(Tour, slug=slug)
    check= Member_on_tour.objects.all().filter(tour=tour, name=request.user)
    context= {'tour':tour,'check':check}
    return render(request,templates,context)

def my_tour_details(request,slug):
    templates= 'tourrelated/manage.html'
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

def managetour(request):
    templates= 'tourrelated/manage_tour.html'
    mytour= Tour.objects.all().filter(creator=request.user)
    context={'tour':mytour}
    return render(request,templates,context)

def alltour(request):
    templates='tourrelated/alltour.html'
    alltour=Tour.objects.all().order_by('-pk')
    context={'alltour':alltour}
    return render(request,templates,context)

def jointour(request):
    templates='tourrelated/jointour.html'
    tour=Member_on_tour.objects.filter(name=request.user.username)
    tour1= Tour.objects.filter(creator=request.user)
    context={'tour':tour,'t':tour1}
    return render(request,templates,context)

def join_tour_manage(request,pk):
    tour=get_object_or_404(Tour, pk=pk)
    sch=Schedule.objects.filter(tour__pk=pk)
    templates= 'tourrelated/join_manage.html'
    if request.method=="POST":
        post=Post()
        post.user=request.user
        post.tour=tour
        post.post=request.POST.get('post')
        post.save()
        return redirect('join_tour_manage',pk=pk)

    post_1=Post.objects.filter(tour__pk=pk)
    try:
        sc=get_object_or_404(Schedule, tour__pk=pk)
        context={'sch':sch,'s':sc,'tour':tour,'post':post_1}
    except:
        context={'sch':sch,'no':'No sachedule','tour':tour,'post':post_1}
    return render(request,templates,context)

def viewmember(request,pk):
    templates='tourrelated/member.html'
    member=Member_on_tour.objects.filter(tour__pk=pk)
    context={'member':member}
    return render(request,templates,context)
