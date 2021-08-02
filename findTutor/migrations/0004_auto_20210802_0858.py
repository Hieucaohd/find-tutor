# Generated by Django 3.2.4 on 2021-08-02 08:58

from django.db import migrations, models
import findTutor.validators


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0003_auto_20210802_0838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprimaryinformation',
            name='location',
        ),
        migrations.AddField(
            model_name='userprimaryinformation',
            name='detail_location',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userprimaryinformation',
            name='district_code',
            field=models.IntegerField(default=1, validators=[findTutor.validators.min_code_of_location, findTutor.validators.max_code_of_district]),
        ),
        migrations.AddField(
            model_name='userprimaryinformation',
            name='province_code',
            field=models.IntegerField(default=1, validators=[findTutor.validators.min_code_of_location, findTutor.validators.max_code_of_province]),
        ),
        migrations.AddField(
            model_name='userprimaryinformation',
            name='ward_code',
            field=models.IntegerField(default=1, validators=[findTutor.validators.min_code_of_location, findTutor.validators.max_code_of_ward]),
        ),
        migrations.AlterField(
            model_name='parentroommodel',
            name='district_code',
            field=models.IntegerField(default=1, validators=[findTutor.validators.min_code_of_location, findTutor.validators.max_code_of_district]),
        ),
        migrations.AlterField(
            model_name='parentroommodel',
            name='province_code',
            field=models.IntegerField(default=1, validators=[findTutor.validators.min_code_of_location, findTutor.validators.max_code_of_province]),
        ),
        migrations.AlterField(
            model_name='parentroommodel',
            name='ward_code',
            field=models.IntegerField(default=1, validators=[findTutor.validators.min_code_of_location, findTutor.validators.max_code_of_ward]),
        ),
    ]
