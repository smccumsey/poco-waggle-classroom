# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-07 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waggle', '0059_auto_20160906_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentSubission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessmentprogresses', models.ManyToManyField(related_name='submissions', to='waggle.AssessmentProgress')),
            ],
        ),
    ]
