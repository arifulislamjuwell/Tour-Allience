from django.urls import path
from . import views

urlpatterns = [
     path('index/',views.index, name='index' ),
     path ('all-tour/<str:slug>/',views.all_tour_details,name='all_tour_details'),
     path ('my-tour/<str:slug>/',views.my_tour_details,name='my_tour_details'),
     path ('join/<int:pk>/',views.joining, name='join'),

     path('add-member/<int:pk>/',views.add_member, name='add_member'),
     path ('expense/<int:pk>/',views.expense, name='expense'),
     path ('schedule/<int:pk>/',views.schedule, name='schedule')


]
