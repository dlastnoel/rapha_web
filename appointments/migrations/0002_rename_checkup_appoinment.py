# Generated by Django 4.0.2 on 2022-03-24 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0020_chiefcomplaint_unicode_presentillness_unicode_and_more'),
        ('doctors', '0022_alter_schedule_weekday_delete_patientcheckup'),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Checkup',
            new_name='Appoinment',
        ),
    ]