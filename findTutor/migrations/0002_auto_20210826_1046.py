# Generated by Django 3.2.4 on 2021-08-26 10:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('findTutor', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ImageOfUser',
            new_name='ImageOfUserModel',
        ),
        migrations.RenameModel(
            old_name='ImagePrivateUser',
            new_name='ImagePrivateUserModel',
        ),
    ]