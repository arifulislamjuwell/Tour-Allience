from django.shortcuts import render,redirect,get_object_or_404
from .models import CreateTour

# Create your views here.

def index(request):
    templates= 'index.html'
    alltour= CreateTour.objects.all()
    usertour=alltour.filter(creator=request.user)
    context={'alltour':alltour,'usertour':usertour}
    if request.method=='POST':
        tour= CreateTour()
        tour.creator=request.user
        tour.title=request.POST.get('title')
        tour.location=request.POST.get('location')
        tour.duration=request.POST.get('duration')
        tour.date_of_tour=request.POST.get('date')
        tour.fee =request.POST.get('fee')
        tour.short_description= request.POST.get('description')
        tour.save()
        return redirect('index')

    return render(request,templates,context)
