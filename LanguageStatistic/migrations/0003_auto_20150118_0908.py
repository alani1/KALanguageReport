# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('LanguageStatistic', '0002_auto_20150118_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtitle',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 18, 9, 8, 57, 62083, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
