# Generated by Django 3.2.4 on 2021-09-08 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0019_rename_teacher_pricemodel_type_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutormodel',
            name='mon_day',
            field=models.TextField(blank=True, null=True),
        ),
    ]
