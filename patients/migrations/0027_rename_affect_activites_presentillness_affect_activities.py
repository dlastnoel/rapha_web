# Generated by Django 4.0.3 on 2022-04-21 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0026_alter_presentillness_describe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presentillness',
            old_name='affect_activites',
            new_name='affect_activities',
        ),
    ]