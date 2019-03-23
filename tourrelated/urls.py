from django.urls import path
from . import views

urlpatterns = [
     path('index/',views.index, name='index' ),
     path ('all-tour/<int:pk>/',views.all_tour_details,name='all_tour_details')

]
