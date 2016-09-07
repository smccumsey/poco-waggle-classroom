# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-01 20:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('waggle', '0052_moduleprogress_started'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionRecord',
            fields=[
                ('record', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='waggle.AssessmentProgress')),
            ],
        ),
        migrations.AddField(
            model_name='assessmentprogress',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 9, 1, 20, 10, 33, 8182, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
