# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0003_log_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puzzle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_name', models.CharField(max_length=255)),
                ('hint', models.TextField()),
                ('solution', models.TextField()),
                ('game', models.ForeignKey(to='station.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
