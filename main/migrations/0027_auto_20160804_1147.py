# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-04 18:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20160804_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_submission', models.TextField()),
                ('submission_feedback', models.TextField()),
                ('assessment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Assessment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Student')),
            ],
        ),
        migrations.CreateModel(
            name='ContentProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_notes', models.TextField()),
                ('video_timepoint', models.DecimalField(decimal_places=2, max_digits=5)),
                ('notebook_download_count', models.PositiveSmallIntegerField()),
                ('content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Content')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Student')),
            ],
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='date_enrolled',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 4, 18, 47, 10, 909792, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='assessment_progress',
            field=models.ManyToManyField(through='main.AssessmentProgress', to='main.Assessment'),
        ),
        migrations.AddField(
            model_name='student',
            name='content_progress',
            field=models.ManyToManyField(through='main.ContentProgress', to='main.Content'),
        ),
    ]