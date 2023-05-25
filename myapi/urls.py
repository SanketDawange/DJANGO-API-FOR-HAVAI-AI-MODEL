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

    # Doctor side's urls
    path('doctor_signup', views.doctor_signup, name='doctor_signup'),
    path('doctor_signin', views.doctor_signin, name='doctor_signin'),
    path('doctor_logout', views.doctor_logout, name='doctor_logout'),
    path('doctor_dashboard', views.doctor_dashboard, name='doctor_dashboard'),


    
    path('getCategories/', views.getCategories, name='getCategories'),
    path('getSchemes/<str:category>', views.getSchemes, name='getSchemes'),
    path('getHospitals/<str:scheme>', views.getHospitals, name='getHospitals'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
