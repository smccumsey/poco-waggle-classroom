# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-02 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waggle', '0055_auto_20160902_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='code_editor_filler',
            field=models.TextField(blank=True, null=True),
        ),
    ]