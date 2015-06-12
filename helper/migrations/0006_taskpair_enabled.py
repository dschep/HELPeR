# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0005_auto_20150611_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskpair',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
