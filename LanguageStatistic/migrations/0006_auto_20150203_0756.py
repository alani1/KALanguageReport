# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('LanguageStatistic', '0005_auto_20150125_0447'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='DARI',
            field=models.CharField(default=b'', max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subtitle',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 3, 7, 56, 55, 974088, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
