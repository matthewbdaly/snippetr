# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2014, 10, 26, 16, 1, 7, 162727, tzinfo=utc))),
                ('slug', models.SlugField(unique=True, max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
