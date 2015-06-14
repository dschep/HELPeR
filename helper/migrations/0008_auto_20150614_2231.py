# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0007_auto_20150612_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentconfig',
            name='options',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
    ]
