from re import template
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from . forms import UserPasswordResetForm

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/edit/', views.editDoctor, name='edit-doctor'),
    path('delete-doctor/<str:pk>/', views.deleteDoctor, name='delete-doctor'),
    path('doctor/<str:pk>/', views.doctorProfile, name='doctor-profile'),
    path('activate/<str:pk>', views.activate, name='activate'),
    path('deactivate/<str:pk>', views.deactivate, name='deactivate'),
    path('specializations/', views.specializations, name='specializations'),
    path('delete-specialization/<str:pk>/',
         views.deleteSpecialization, name='delete-specialization'),
    path('edit-specialization/<str:pk>/',
         views.editSpecialization, name='edit-specialization'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='doctors/reset_password.html',
         form_class=UserPasswordResetForm), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='doctors/reset_password_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='doctors/reset.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='doctors/reset_password_complete.html'),
         name='password_reset_complete'),
]
