# Generated by Django 3.2.4 on 2021-08-31 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0009_auto_20210830_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageofusermodel',
            name='is_using',
            field=models.BooleanField(default=True),
        ),
    ]