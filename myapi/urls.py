from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('getResponse/<str:user_message>', views.getResponse, name='getResponse'),
    path('makeAppointment/<str:user_message>', views.makeAppointment, name='makeAppointment'),
    path('signUp/<str:username>/<str:password>', views.signUp, name='signUp'),
    path('loginUser/<str:username>/<str:password>', views.loginUser, name='loginUser'),
    path('getUserDetails/<str:username>', views.getUserDetails, name='getUserDetails'),
    path('getUserDocs/<str:username>/<str:key>', views.getUserDocs, name='getUserDocs'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
