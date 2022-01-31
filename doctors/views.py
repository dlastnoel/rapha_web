from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from . forms import *


def loginUser(request):
    if(request.user.is_authenticated):
        return redirect('dashboard')

    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_login = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user_login = authenticate(
            request, username=username, password=password)
        if user_login is not None:
            doctor = Doctor.objects.get(user=user_login)
            if doctor.is_activated:
                login(request, user_login)
                return redirect('dashboard')
            else:
                messages.error(request, 'Account is deactivated')
        else:
            messages.error(request, 'Username or password is incorrect')

    context = {
        'title': 'Login'
    }
    return render(request, 'doctors/login_register.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    user_form = UserForm(prefix='usr')
    doctor_form = DoctorForm(prefix='dr')

    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='usr')
        doctor_form = DoctorForm(request.POST, request.FILES, prefix='dr')
        if user_form.is_valid() and doctor_form.is_valid():
            doctor_data = doctor_form.cleaned_data
            user_form.save()
            last_user = User.objects.last()
            doctor = Doctor.objects.get(user=last_user)
            doctor.specialization = doctor_data['specialization']
            doctor.middle_name = doctor_data['middle_name']
            doctor.address = doctor_data['address']
            doctor.contact = doctor_data['contact']
            doctor.schedule = doctor_data['schedule']
            doctor.short_bio = doctor_data['short_bio']
            doctor.save()

            messages.success(
                request, 'Registration sent, wait for your account activation')
            return redirect('login')

        else:
            messages.error(
                request, 'An error has occurred during registration')

    context = {
        'title': 'Register',
        'user_form': user_form,
        'doctor_form': doctor_form,
    }
    return render(request, 'doctors/login_register.html', context)


@login_required(login_url='login')
def dashboard(request):
    title = 'Dashboard'
    is_admin = request.user.is_superuser
    doctor = request.user.doctor
    nav_active = 'nav-active'
    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active
    }

    return render(request, 'doctors/dashboard.html', context)


@login_required(login_url='login')
def doctors(request):
    title = 'Doctors'
    is_admin = request.user.is_superuser
    doctor = request.user.doctor
    doctors = Doctor.objects.all()
    nav_active = 'nav-active'
    context = {
        'title': title,
        'doctor': doctor,
        'doctors': doctors,
        'is_admin': is_admin,
        'nav_active': nav_active
    }

    return render(request, 'doctors/doctors.html', context)


@login_required(login_url='login')
def deleteDoctor(request, pk):
    if request.user.is_superuser:
        doctor = Doctor.objects.get(id=pk)
        doctor.delete()
        return redirect('doctors')
    else:
        return redirect('dashboard')


@login_required(login_url='login')
def doctorProfile(request, pk):
    title = 'Doctors'
    is_admin = request.user.is_superuser
    doctor = Doctor.objects.get(id=pk)
    nav_active = 'nav-active'
    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active
    }
    return render(request, 'doctors/view.html', context)


@login_required(login_url='login')
def editDoctor(request):
    title = 'Doctors'
    is_admin = request.user.is_superuser
    doctor = request.user.doctor
    nav_active = 'nav-active'
    user_form = UserForm(instance=request.user, prefix='usr-in')
    doctor_form = NewDoctorForm(
        instance=doctor, prefix='dr-in')

    if request.method == 'POST':
        user_form = UserForm(
            request.POST, instance=request.user, prefix='usr-in')
        doctor_form = NewDoctorForm(
            request.POST, request.FILES, instance=request.user.doctor, prefix='dr-in')
        if user_form.is_valid() and doctor_form.is_valid():
            # doctor_data = doctor_form.cleaned_data
            # last_user = User.objects.last()
            # doctor = Doctor.objects.get(user=last_user)
            # doctor.profile_image = doctor_data['profile_image']
            # doctor.specialization = doctor_data['specialization']
            # doctor.middle_name = doctor_data['middle_name']
            # doctor.address = doctor_data['address']
            # doctor.contact = doctor_data['contact']
            # doctor.schedule = doctor_data['schedule']
            # doctor.short_bio = doctor_data['short_bio']
            user_form.save()
            doctor_form.save()

            user_login = authenticate(
                request, username=request.user.username, password=request.user.password)
            login(request, user_login)
            return redirect('dashboard')

        else:
            print('Error')
            messages.error(
                request, 'An error has occurred during doctor update')

    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'user_form': user_form,
        'doctor_form': doctor_form,
    }

    return render(request, 'doctors/doctor-form.html', context)


@login_required(login_url='login')
def activate(request, pk):
    doctor = Doctor.objects.get(id=pk)
    doctor.is_activated = True
    doctor.save()

    return redirect('doctors')


@login_required(login_url='login')
def deactivate(request, pk):
    if request.user.is_superuser:
        doctor = Doctor.objects.get(id=pk)
        doctor.is_activated = False
        doctor.save()
    else:
        return redirect('dashboard')

    return redirect('doctors')


@login_required(login_url='login')
def specializations(request):
    if request.user.is_superuser:
        specializations = Specialization.objects.all()
        title = 'Specializations'
        is_admin = request.user.is_superuser
        doctor = request.user.doctor
        nav_active = 'nav-active'
        function = 'add'
        speciliazation_form = SpecilizationForm()
        if request.method == 'POST':
            speciliazation_form = SpecilizationForm(request.POST)
            if speciliazation_form.is_valid():
                speciliazation_form.save()
                return redirect('specializations')
        context = {
            'title': title,
            'doctor': doctor,
            'is_admin': is_admin,
            'function': function,
            'nav_active': nav_active,
            'specializations': specializations,
            'specialization_form': speciliazation_form,
        }

        return render(request, 'doctors/specializations.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='login')
def deleteSpecialization(request, pk):
    if request.user.is_superuser:
        specialization = Specialization.objects.get(id=pk)
        specialization.delete()
        return redirect('specializations')
    else:
        return redirect('dashboard')


@login_required(login_url='login')
def editSpecialization(request, pk):
    if request.user.is_superuser:
        specializations = Specialization.objects.all()
        title = 'Specializations'
        is_admin = request.user.is_superuser
        doctor = request.user.doctor
        nav_active = 'nav-active'
        active_specialization = Specialization.objects.get(id=pk)
        function = 'edit'
        speciliazation_form = SpecilizationForm(instance=active_specialization)
        if request.method == 'POST':
            speciliazation_form = SpecilizationForm(
                request.POST, instance=active_specialization)
            if speciliazation_form.is_valid():
                speciliazation_form.save()
                return redirect('specializations')
        context = {
            'title': title,
            'doctor': doctor,
            'is_admin': is_admin,
            'function': function,
            'nav_active': nav_active,
            'specializations': specializations,
            'active_specialization': active_specialization,
            'specialization_form': speciliazation_form,
        }

        return render(request, 'doctors/specializations.html', context)
    else:
        return redirect('dashboard')
