# Generated by Django 4.0 on 2022-01-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0008_alter_doctor_address_alter_doctor_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='is_activated',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
