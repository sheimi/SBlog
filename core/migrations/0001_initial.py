# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(max_length=128)),
                ('url', models.CharField(serialize=False, primary_key=True, max_length=128)),
                ('author', models.CharField(max_length=32)),
                ('location', models.CharField(max_length=32)),
                ('date', models.DateTimeField()),
                ('content', models.TextField()),
                ('content_thumbnail', models.TextField()),
                ('show_in_home', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='core.Category', related_name='posts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='core.Tag', related_name='posts'),
            preserve_default=True,
        ),
    ]
