# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-03 17:51
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_auto_20160902_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='assess_file',
            field=models.FileField(blank=True, null=True, upload_to=main.models.assessment_directory_path),
        ),
    ]