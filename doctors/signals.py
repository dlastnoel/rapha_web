from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from . models import Doctor, Schedule


def createDoctor(sender, instance, created, **kwargs):
    my_user = instance
    if created:
        doctor = Doctor.objects.create(
            user=my_user,
            username=my_user.username,
            first_name=my_user.first_name,
            last_name=my_user.last_name,
            email=my_user.email
        )
        last_doctor = Doctor.objects.latest('created_at')
        weekday_choices = ['Monday', 'Tuesday',
                           'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        i = 0
        while(i <= 6):
            schedule = Schedule.objects.create(
                doctor=last_doctor,
                weekday=weekday_choices[i]
            )
            i += 1
            schedule.save()

    else:
        doctor = Doctor.objects.get(user=my_user)
        doctor.email = my_user.email
        doctor.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createDoctor, sender=User)
post_delete.connect(deleteUser, sender=Doctor)
