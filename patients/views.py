from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
# Create your views here.


@login_required(login_url='login')
def patients(request):
    title = 'Patients'
    is_admin = request.user.is_superuser
    doctor = request.user.doctor
    nav_active = 'nav-active'
    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active
    }
    return render(request, 'patients/index.html', context)