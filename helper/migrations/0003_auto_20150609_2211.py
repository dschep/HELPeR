# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0002_taskpair'),
    ]

    operations = [
        migrations.CreateModel(
            name='DedupEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('task', models.CharField(max_length=255)),
                ('key', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='dedupevent',
            unique_together=set([('task', 'key')]),
        ),
    ]
