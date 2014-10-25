# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0002_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='title',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
