# Generated by Django 3.2.10 on 2022-01-05 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freshman', '0002_auto_20220105_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freshman',
            name='student_id',
        ),
    ]
