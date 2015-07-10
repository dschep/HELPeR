# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore
from django.contrib.postgres.operations import HStoreExtension


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name='AgentConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('options', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
        ),
    ]
