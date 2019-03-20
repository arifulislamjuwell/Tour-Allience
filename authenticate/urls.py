from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login, name= 'login'),
    path('Registration/',views.registration, name='registration'),
    path('logout/',views.logout, name= 'logout')

]
