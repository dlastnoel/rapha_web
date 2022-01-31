from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from . models import Doctor


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
    else:
        doctor = Doctor.objects.get(user=my_user)
        doctor.email = my_user.email
        doctor.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createDoctor, sender=User)
post_delete.connect(deleteUser, sender=Doctor)
