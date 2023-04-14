from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getResponse/<str:user_message>', views.getResponse, name='getResponse'),
    path('makeAppointment/<str:user_message>', views.makeAppointment, name='makeAppointment'),
    path('signUp/<str:username>/<str:password>', views.signUp, name='signUp'),
    path('loginUser/<str:username>/<str:password>', views.loginUser, name='loginUser'),
]
