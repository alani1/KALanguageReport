# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('LanguageStatistic', '0004_auto_20150125_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtitle',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 4, 47, 35, 499717, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='ARABIC',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='ARMENIAN',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='BAHASA_INDONESIA',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='BANGLA',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='BULGARIAN',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='CHINESE',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='CZECH',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='DANISH',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='DEUTSCH',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='ENGLISH',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='ESPANOL',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='FARSI',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='FRANCAIS',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='GREEK',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='HEBREW',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='ITALIANO',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='JAPANESE',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='KISWAHILI',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='KOREAN',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='MONGOLIAN',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='NEDERLANDS',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='NEPALI',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='NORSK',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='POLISH',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='PORTUGAL_PORTUGUES',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='PORTUGUES',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='PUNJABI',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='RUSSIAN',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='SERBIAN',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='SINDHI',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='SINHALA',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='TAMIL',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='TELUGU',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='THAI',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='TURKCE',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='UKRAINIAN',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='URDU',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='XHOSA',
            field=models.CharField(max_length=16, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='ZULU',
            field=models.CharField(max_length=64, blank=True),
            preserve_default=True,
        ),
    ]
