# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 22:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waggle', '0021_auto_20160803_1541'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentProfile',
            new_name='Student',
        ),
        migrations.RenameField(
            model_name='progress',
            old_name='enrolled_courses',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='usr_progress',
            new_name='user_progress',
        ),
    ]
