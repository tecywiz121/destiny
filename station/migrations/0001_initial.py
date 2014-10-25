# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('action', models.IntegerField(choices=[(0, b'Authenticated'), (1, b'Deauthenticated'), (2, b'Personal Log'), (5, b'Announced'), (6, b'Initiated Repair'), (7, b'Disabled System'), (8, b'Enabled System'), (9, '\u2593\u2593\u2593\u2593\u2593\u2593\u2593\u2593\u2593\u2593\u2593\u2593')])),
                ('detail', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(choices=[(0, b'Initial'), (1, b'Overload in progress'), (2, b'Overload aborted'), (3, b'Dead')])),
                ('start_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('status', models.BooleanField(default=True, choices=[(True, b'online'), (False, b'offline')])),
                ('game', models.ForeignKey(related_name=b'systems', to='station.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='system',
            unique_together=set([('game', 'name')]),
        ),
        migrations.AddField(
            model_name='activity',
            name='game',
            field=models.ForeignKey(related_name=b'activities', to='station.Game'),
            preserve_default=True,
        ),
    ]
