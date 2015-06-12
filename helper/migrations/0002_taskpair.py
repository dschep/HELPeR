# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskPair',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('cause_agent', models.CharField(max_length=255)),
                ('cause_task', models.CharField(max_length=255)),
                ('cause_options', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
                ('effect_agent', models.CharField(max_length=255)),
                ('effect_task', models.CharField(max_length=255)),
                ('effect_options', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
            ],
        ),
    ]
