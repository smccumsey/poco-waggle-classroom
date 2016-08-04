# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-04 06:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waggle', '0023_auto_20160803_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='waggle.Course')),
            ],
        ),
        migrations.RemoveField(
            model_name='progress',
            name='module',
        ),
        migrations.RemoveField(
            model_name='progress',
            name='student',
        ),
        migrations.RemoveField(
            model_name='student',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user_progress',
        ),
        migrations.DeleteModel(
            name='Progress',
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waggle.Student'),
        ),
        migrations.AddField(
            model_name='student',
            name='course_progress',
            field=models.ManyToManyField(through='waggle.CourseProgress', to='waggle.Course'),
        ),
    ]
