# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_name(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    TaskPair = apps.get_model('helper', 'TaskPair')
    for taskpair in TaskPair.objects.all():
        taskpair.name = '{}:{} -> {}:{}'.format(
            taskpair.cause_agent, taskpair.cause_task,
            taskpair.effect_agent, taskpair.effect_task,
        )
        taskpair.save()


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0008_auto_20150614_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskpair',
            name='name',
            field=models.CharField(null=True, max_length=255, blank=True),
        ),
        migrations.RunPython(populate_name, lambda app, schema_editor: None),
    ]
