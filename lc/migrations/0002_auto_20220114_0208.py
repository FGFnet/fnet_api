# Generated by Django 3.2.10 on 2022-01-14 02:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lc', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lc',
            options={'ordering': ['schedule', 'name']},
        ),
        migrations.RemoveField(
            model_name='lc',
            name='fg',
        ),
        migrations.RemoveField(
            model_name='lc',
            name='total',
        ),
        migrations.AddField(
            model_name='lc',
            name='fg_n',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fg_n', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lc',
            name='fg_s',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fg_s', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lc',
            name='schedule',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
