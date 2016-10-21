# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-29 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import kpcc_backroom_handshakes.custom_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(b'Primary', b'Primary'), (b'General', b'General'), (b'Special', b'Special')], default=b'Primary', max_length=255, verbose_name=b'Type of Election')),
                ('electionid', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Election ID')),
                ('test_results', models.BooleanField(default=False, verbose_name=b'Are These Test Results')),
                ('live_results', models.BooleanField(default=False, verbose_name=b'Are These Live Results')),
                ('election_date', models.DateField(blank=True, null=True, verbose_name=b'Date of the Election')),
                ('poll_close_at', models.DateTimeField(blank=True, null=True, verbose_name=b'Time Polls Close')),
                ('national', models.BooleanField(default=False, verbose_name=b'Is National Election?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'Date Modified')),
            ],
        ),
        migrations.CreateModel(
            name='ResultSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name=b'Data Source Name')),
                ('source_short', models.CharField(max_length=5, verbose_name=b'Data Source Shortname')),
                ('source_slug', models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name=b'Slugged Data Source')),
                ('source_url', models.URLField(blank=True, max_length=1024, null=True, verbose_name=b'Url To Data Source')),
                ('source_active', models.BooleanField(default=False, verbose_name=b'Active Data Source?')),
                ('source_type', models.CharField(max_length=255, verbose_name=b'Ext Of File Or Type Of Source')),
                ('source_files', kpcc_backroom_handshakes.custom_fields.ListField(blank=True, null=True, verbose_name=b'Results Files We Want')),
                ('source_latest', models.DateTimeField(blank=True, null=True, verbose_name=b'Latest Results From')),
                ('source_created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('source_modified', models.DateTimeField(auto_now=True, verbose_name=b'Date Modified')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election_registrar.Election')),
            ],
        ),
    ]