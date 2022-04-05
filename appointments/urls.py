from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('appointments/', views.appointments, name='appointments'),
    path('appointment/<str:pk>/', views.appointment, name='appointment'),
    path('appointment/admit/<str:pk>', views.admitPatient, name='admit'),
]
