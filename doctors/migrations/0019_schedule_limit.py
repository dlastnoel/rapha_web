# Generated by Django 4.0.2 on 2022-03-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0018_alter_schedule_end_alter_schedule_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='limit',
            field=models.TimeField(blank=True, null=True),
        ),
    ]