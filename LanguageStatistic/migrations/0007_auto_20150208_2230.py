# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('LanguageStatistic', '0006_auto_20150203_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtitle',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 8, 22, 30, 27, 764247, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='AMARA_ID',
            field=models.CharField(db_index=True, max_length=16, blank=True),
            preserve_default=True,
        ),
    ]
