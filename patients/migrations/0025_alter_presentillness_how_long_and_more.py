# Generated by Django 4.0.3 on 2022-04-21 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0024_presentillness_affect_activites_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentillness',
            name='how_long',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='presentillness',
            name='how_often',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='presentillness',
            name='symptoms_started',
            field=models.DateField(blank=True, null=True),
        ),
    ]
