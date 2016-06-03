# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-10 22:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ballot_box', '0009_candidate'),
    ]

    operations = [
        migrations.CreateModel(
            name='BallotMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measureid', models.CharField(max_length=255, verbose_name='Candidate ID')),
                ('ballotorder', models.IntegerField(blank=True, null=True, verbose_name='Numerical Position On The Ballot')),
                ('name', models.CharField(max_length=255, verbose_name='Name of Ballot Measure')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description Of Ballot Measure')),
                ('yescount', models.IntegerField(blank=True, null=True, verbose_name='Number Of Yes Votes Received')),
                ('yespct', models.FloatField(blank=True, null=True, verbose_name='Percent Of Yes Votes Received')),
                ('nocount', models.IntegerField(blank=True, null=True, verbose_name='Number Of Yes Votes Received')),
                ('nopct', models.FloatField(blank=True, null=True, verbose_name='Percent Of Yes Votes Received')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Date Modified')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ballot_box.Contest')),
            ],
        ),
    ]
