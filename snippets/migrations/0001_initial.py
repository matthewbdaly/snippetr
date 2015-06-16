# -*- coding: utf-8 -*-
from django.db import models, migrations
import django.utils.timezone


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
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(unique=True, max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
