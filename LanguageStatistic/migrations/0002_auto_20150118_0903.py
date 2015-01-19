# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import jsonfield.fields
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('LanguageStatistic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtitle',
            name='author',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subtitle',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 18, 9, 3, 17, 802507, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subtitle',
            name='infoData',
            field=jsonfield.fields.JSONField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subtitle',
            name='lines',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subtitle',
            name='origLines',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='DATE_ADDED',
            field=models.DateField(verbose_name=b'Updated'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='DATE_CREATED',
            field=models.DateField(verbose_name=b'Date'),
            preserve_default=True,
        ),
    ]
