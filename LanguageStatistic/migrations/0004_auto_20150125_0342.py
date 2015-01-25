# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('LanguageStatistic', '0003_auto_20150118_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='showsExercise',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subtitle',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 3, 42, 24, 391518, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
