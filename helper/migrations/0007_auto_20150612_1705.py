# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0006_taskpair_enabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agentconfig',
            name='id',
        ),
        migrations.AlterField(
            model_name='agentconfig',
            name='name',
            field=models.CharField(primary_key=True, serialize=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='taskpair',
            name='cause_agent',
            field=models.ForeignKey(related_name='cause_task_pairs', to='helper.AgentConfig'),
        ),
        migrations.AlterField(
            model_name='taskpair',
            name='effect_agent',
            field=models.ForeignKey(related_name='effect_task_pairs', to='helper.AgentConfig'),
        ),
    ]
