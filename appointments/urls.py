from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('appointments/', views.appointments, name='appointments'),
    path('appointment/<str:pk>/', views.appointment, name='appointment'),
    path('appointment/admit/<str:pk>', views.admitPatient, name='admit'),
    path('appointment/previous/<str:pk>', views.previous, name='previous'),
    path('appointments/future/', views.futureAppointments, name='future'),
    path('appointment/cancel-and-refer/<str:pk>',
         views.cancelAndReferAppointment, name='cancel-and-refer'),
    path('appointment/cancel-appointment/<str:pk>',
         views.cancelAppointment, name='cancel-appointment'),
]
