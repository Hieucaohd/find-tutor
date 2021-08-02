# Generated by Django 3.2.4 on 2021-08-01 17:26

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('findTutor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parentroommodel',
            name='detail_location',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='parentroommodel',
            name='other_require',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='tutormodel',
            name='achievement',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='tutormodel',
            name='cap_day',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'cap_1'), (2, 'cap_2'), (3, 'cap_3'), (4, 'dai_hoc')], max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='tutormodel',
            name='experience',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='tutormodel',
            name='khu_vuc_day',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='tutormodel',
            name='lop_day',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'lop_1'), (2, 'lop_2'), (3, 'lop_3'), (4, 'lop_4'), (5, 'lop_5'), (6, 'lop_6'), (7, 'lop_7'), (8, 'lop_8'), (9, 'lop_9'), (10, 'lop_10'), (11, 'lop_11'), (12, 'lop_12'), (13, 'nam_1'), (14, 'nam_2'), (15, 'nam_3'), (16, 'nam_4'), (17, 'nam_5')], max_length=41, null=True),
        ),
        migrations.AlterField(
            model_name='tutormodel',
            name='profession',
            field=models.CharField(choices=[('sv', 'SINH_VIEN'), ('gv', 'GIAO_VIEN')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='tutormodel',
            name='university',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprimaryinformation',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='userprimaryinformation',
            name='birthday',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userprimaryinformation',
            name='identity_card',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='userprimaryinformation',
            name='location',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprimaryinformation',
            name='number_of_identity_card',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userprimaryinformation',
            name='number_phone',
            field=models.CharField(max_length=30, null=True),
        ),
    ]