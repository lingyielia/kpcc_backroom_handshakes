# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-03 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election_registrar', '0002_election_election_caveats'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultsource',
            name='ready_to_build',
            field=models.BooleanField(default=False, verbose_name=b'Build This Source'),
        ),
    ]
