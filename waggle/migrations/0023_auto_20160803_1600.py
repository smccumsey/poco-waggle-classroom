# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 23:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waggle', '0022_auto_20160803_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progress',
            name='course',
        ),
        migrations.AddField(
            model_name='progress',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waggle.Module'),
        ),
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(to='waggle.Course'),
        ),
        migrations.AlterField(
            model_name='student',
            name='user_progress',
            field=models.ManyToManyField(through='waggle.Progress', to='waggle.Module'),
        ),
    ]
