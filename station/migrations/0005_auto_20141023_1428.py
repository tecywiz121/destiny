# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0004_puzzle'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='solved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='puzzle',
            unique_together=set([('game', 'url_name')]),
        ),
    ]
