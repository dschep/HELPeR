# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0004_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='dedupevent',
            name='task_pair',
            field=models.ForeignKey(default=1, to='helper.TaskPair'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='dedupevent',
            unique_together=set([('task_pair', 'key')]),
        ),
        migrations.RemoveField(
            model_name='dedupevent',
            name='task',
        ),
    ]
