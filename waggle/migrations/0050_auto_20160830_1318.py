# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-30 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waggle', '0049_auto_20160826_1553'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseprogress',
            old_name='registered',
            new_name='approved',
        ),
        migrations.AlterField(
            model_name='courseprogress',
            name='date_enrolled',
            field=models.DateTimeField(blank=True),
        ),
    ]
