# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0005_auto_20141023_1428'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='puzzle',
            unique_together=None,
        ),
    ]
