# Generated by Django 4.0.2 on 2022-03-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0017_alter_schedule_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
