# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-28 05:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email_address',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]