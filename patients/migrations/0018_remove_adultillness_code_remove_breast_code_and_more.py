# Generated by Django 4.0.2 on 2022-03-07 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0017_adultillness_code_breast_code_cardiovascular_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adultillness',
            name='code',
        ),
        migrations.RemoveField(
            model_name='breast',
            name='code',
        ),
        migrations.RemoveField(
            model_name='cardiovascular',
            name='code',
        ),
        migrations.RemoveField(
            model_name='chiefcomplaint',
            name='code',
        ),
        migrations.RemoveField(
            model_name='childhoodillness',
            name='code',
        ),
        migrations.RemoveField(
            model_name='endocrine',
            name='code',
        ),
        migrations.RemoveField(
            model_name='familyhistory',
            name='code',
        ),
        migrations.RemoveField(
            model_name='functionalhistory',
            name='code',
        ),
        migrations.RemoveField(
            model_name='gastrointestinal',
            name='code',
        ),
        migrations.RemoveField(
            model_name='generalsystem',
            name='code',
        ),
        migrations.RemoveField(
            model_name='genitourinary',
            name='code',
        ),
        migrations.RemoveField(
            model_name='gynecologic',
            name='code',
        ),
        migrations.RemoveField(
            model_name='heent',
            name='code',
        ),
        migrations.RemoveField(
            model_name='historyofimmunization',
            name='code',
        ),
        migrations.RemoveField(
            model_name='musculoskeletal',
            name='code',
        ),
        migrations.RemoveField(
            model_name='neurologic',
            name='code',
        ),
        migrations.RemoveField(
            model_name='personalandsocialhistory',
            name='code',
        ),
        migrations.RemoveField(
            model_name='presentillness',
            name='code',
        ),
        migrations.RemoveField(
            model_name='pulmonary',
            name='code',
        ),
        migrations.RemoveField(
            model_name='skinproblem',
            name='code',
        ),
        migrations.AddField(
            model_name='childhoodillness',
            name='unicode',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
