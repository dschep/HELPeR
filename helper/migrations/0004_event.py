# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0003_auto_20150609_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('task_type', models.CharField(choices=[('cause', 'cause'), ('effect', 'effect')], max_length=255)),
                ('data', django.contrib.postgres.fields.hstore.HStoreField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('task_pair', models.ForeignKey(to='helper.TaskPair')),
            ],
        ),
    ]
