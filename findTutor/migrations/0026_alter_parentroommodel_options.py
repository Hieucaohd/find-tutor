# Generated by Django 3.2.4 on 2021-11-07 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0025_auto_20211102_0715'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parentroommodel',
            options={'permissions': (('delete_room', 'Delete a room'),)},
        ),
    ]
