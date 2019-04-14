from django.urls import path
from . import views

urlpatterns = [
     path ('all-tour/<str:slug>/',views.all_tour_details,name='all_tour_details'),
     path ('my-tour/<str:slug>/',views.my_tour_details,name='my_tour_details'),
     path ('join/<int:pk>/',views.joining, name='join'),
     path ('manage-tour/',views.managetour,name='manage'),
     path ('all-tour/',views.alltour, name='alltour'),
     path ('join-tour/',views.jointour,name='jointour'),
     path ('join-tour/<int:pk>/',views.join_tour_manage,name='join_tour_manage'),
     path ('create-tour/',views.cratetour,name='createtour'),
     path ('view-member/<int:pk>/',views.viewmember,name='member'),

     path('add-member/<int:pk>/',views.add_member, name='add_member'),
     path ('expense/<int:pk>/',views.expense, name='expense'),
     path ('schedule/<int:pk>/',views.schedule, name='schedule')


]
