# Generated by Django 4.0.2 on 2022-03-14 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0012_remove_doctor_schedule_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='weekday',
            field=models.CharField(choices=[('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday'), ('SATURDAY', 'Saturday'), ('SUNDAY', 'Sunday')], max_length=100),
        ),
    ]
