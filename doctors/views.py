from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from patients.models import ChiefComplaint
from clients.models import Client
from . forms import *
from datetime import datetime, date, timedelta
from django.db.models import Count
from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractDay
from appointments.models import Appoinment

# from io import BytesIO
# from django.http import HttpResponse
# from django.template.loader import get_template
# from django.views import View
# from xhtml2pdf import pisa


# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None


# data = {
#     "company": "Dennnis Ivanov Company",
#     "address": "123 Street name",
#     "city": "Vancouver",
#     "state": "WA",
#     "zipcode": "98663",


#     "phone": "555-555-2345",
#     "email": "youremail@dennisivy.com",
#     "website": "dennisivy.com",
# }

# # Opens up page as PDF


# class ViewPDF(View):
#     def get(self, request, *args, **kwargs):

#         pdf = render_to_pdf('doctors/pdf_template.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')


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
            doctor.short_bio = doctor_data['short_bio']
            doctor.save()

            messages.success(
                request, 'Registration sent, wait for your account activation')
            return redirect('login')

        else:
            print(doctor_form.errors)
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
    slot = Slot.objects.get(id=1)
    doctor_fields = Doctor.objects.all().values('specialization__field').annotate(
        total=Count('specialization')).order_by('total')
    field_total = Doctor.objects.count()
    stats = Appoinment.objects.values('unicode', 'checkup_date').annotate(
        total=Count('checkup_date')).order_by('total')
    stats_count = 0
    registered_users = Client.objects.count()
    registered_doctors = Doctor.objects.count()
    for stat in stats:
        stats_count = stats_count + stat['total']

    # Starts with knowing the day of the week
    week_day = datetime.now().isocalendar()[2]
    # Calculates Starting date (Sunday) for this case by subtracting current date with time delta of the day of the week
    start_date = datetime.now() - timedelta(days=week_day)
    # Prints the list of dates in a current week
    dates = [((start_date + timedelta(days=i)).date())
             for i in range(7)]
    checkup_dates = []
    counts = []
    symptoms = [
        0,  # cough - 0
        0,  # pain - 1
        0,  # weakness - 2
        0,  # trouble_breathing - 3
        0,  # vomitting - 4
        0,  # voweling - 5
        0  # others - 6
    ]

    i = 0
    while(i < 7):
        checkup_dates.append(dates[i].strftime('%B %d, %Y'))
        counts.append(0)
        i = i+1
    i = 0

    for stat in stats:
        while(i < 7):
            print('DATE: ', dates[i])
            print('CHECKUP DATE: ', stat['checkup_date'])
            if(dates[i] == stat['checkup_date']):
                counts[i] = counts[i]+1
                chief_complaint = ChiefComplaint.objects.get(
                    unicode=stat['unicode'])
                if chief_complaint.cough:
                    symptoms[0] = symptoms[0] + 1
                if chief_complaint.pain:
                    symptoms[1] = symptoms[1] + 1
                if chief_complaint.weakness:
                    symptoms[2] = symptoms[2] + 1
                if chief_complaint.trouble_breathing:
                    symptoms[3] = symptoms[3] + 1
                if chief_complaint.vomitting:
                    symptoms[4] = symptoms[4] + 1
                if chief_complaint.voweling:
                    symptoms[5] = symptoms[5] + 1
                if chief_complaint.others != '':
                    symptoms[6] = symptoms[6] + 1
            i = i+1
        i = 0
    i = 0

    print('SYMPTOMS DATA:', symptoms)

    if slot.limit == date.today():
        slot.limit = date.today() + timedelta(days=14)
        slot.save()

    title = 'Dashboard'
    is_admin = request.user.is_superuser
    doctor = request.user.doctor
    nav_active = 'nav-active'
    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'doctor_fields': doctor_fields,
        'field_total': field_total,
        'stats': stats,
        'stats_count': stats_count,
        'checkup_dates': checkup_dates,
        'counts': counts,
        'symptoms': symptoms,
        'registered_users': registered_users,
        'registered_doctors': registered_doctors,
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
    if request.method == 'POST':
        print('Hello World')
    else:
        print('Hello World')
    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active
    }
    return render(request, 'doctors/view.html', context)


@login_required(login_url='login')
def viewSchedule(request):
    title = 'Manage Schedule'
    profile = request.user.doctor
    doctor = Doctor.objects.get(id=profile.id)
    active_id = 0
    schedules = Schedule.objects.filter(doctor=profile.id)
    schedule_form = ScheduleForm()
    is_admin = request.user.is_superuser
    nav_active = 'nav-active'

    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'active_id': active_id,
        'schedule_form': schedule_form,
        'schedules': schedules,
    }
    return render(request, 'doctors/schedule.html', context)


@login_required(login_url='login')
def editSchedule(request, pk):
    title = 'Manage Schedule'
    profile = request.user.doctor
    doctor = Doctor.objects.get(id=profile.id)
    active_schedule = Schedule.objects.get(id=pk)
    active_id = active_schedule.id
    schedules = Schedule.objects.filter(doctor=profile.id)
    schedule_form = ScheduleForm(instance=active_schedule)
    is_admin = request.user.is_superuser
    nav_active = 'nav-active'

    if request.method == 'POST':
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['doctor'] = profile.id
        request.POST['start'] = datetime.strptime(
            request.POST['start'], "%H:%M").strftime("%I:%M %p")
        request.POST['end'] = datetime.strptime(
            request.POST['end'], "%H:%M").strftime("%I:%M %p")
        request.POST._mutable = mutable
        schedule_form = ScheduleForm(request.POST, instance=active_schedule)
        if schedule_form.is_valid():
            schedule_form.save()
        else:
            print(schedule_form.errors)
        return redirect('schedule')

    context = {
        'title': title,
        'doctor': doctor,
        'is_admin': is_admin,
        'nav_active': nav_active,
        'active_schedule': active_schedule,
        'active_id': active_id,
        'schedule_form': schedule_form,
        'schedules': schedules,
    }
    return render(request, 'doctors/schedule.html', context)


@login_required(login_url='login')
def resetSchedule(request, pk):
    active_schedule = Schedule.objects.get(id=pk)
    active_schedule.start = None
    active_schedule.end = None
    active_schedule.save()

    return redirect('schedule')


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
        specializations = Specialization.objects.filter(soft_delete=False)
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
        specialization.soft_delete = True
        specialization.save()
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
