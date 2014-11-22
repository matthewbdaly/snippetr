# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='snippet',
            name='slug',
            field=models.SlugField(max_length=40, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
