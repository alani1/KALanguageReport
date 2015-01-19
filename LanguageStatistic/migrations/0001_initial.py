# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import jsonfield.fields
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageStatistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=5)),
                ('date', models.DateField(verbose_name=b'date')),
                ('type', models.CharField(max_length=1, choices=[(b'C', b'Crowdin'), (b'D', b'Dubbed'), (b'S', b'Subtitled')])),
                ('target', models.CharField(max_length=1, choices=[(b'T', b'Test'), (b'L', b'Live'), (b'R', b'Rockstar')])),
                ('totalSecs', models.IntegerField(default=0)),
                ('countSecs', models.IntegerField(default=0)),
                ('speedSecs', models.IntegerField(default=0)),
                ('totalStrings', models.IntegerField(default=0)),
                ('countStrings', models.IntegerField(default=0)),
                ('speedStrings', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('speed', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subtitle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amaraID', models.CharField(max_length=16, db_index=True)),
                ('lang', models.CharField(max_length=5, db_index=True)),
                ('completion', models.BooleanField(default=False)),
                ('percentDone', models.FloatField()),
                ('data', jsonfield.fields.JSONField()),
                ('lines', models.IntegerField(default=0)),
                ('origLines', models.IntegerField(default=0)),
                ('infoData', jsonfield.fields.JSONField(default='')),
                ('author', models.CharField(default='', max_length=32)),
                ('title', models.CharField(max_length=256)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 1, 18, 8, 44, 3, 162943, tzinfo=utc))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SERIAL', models.IntegerField()),
                ('DATE_ADDED', models.DateField(verbose_name=b'date')),
                ('DATE_CREATED', models.DateField(verbose_name=b'date')),
                ('TITLE', models.CharField(max_length=128)),
                ('LICENSE', models.CharField(max_length=32)),
                ('DOMAIN', models.CharField(max_length=32)),
                ('SUBJECT', models.CharField(max_length=64)),
                ('TOPIC', models.CharField(max_length=256)),
                ('TUTORIAL', models.CharField(max_length=256)),
                ('TITLE_ID', models.CharField(max_length=256)),
                ('DURATION', models.IntegerField()),
                ('URL', models.CharField(max_length=256)),
                ('AMARA_ID', models.CharField(max_length=16, db_index=True)),
                ('REQUIRED_FOR', models.CharField(max_length=32, db_index=True)),
                ('TRANSCRIPT', models.CharField(max_length=1)),
                ('ENGLISH', models.CharField(max_length=16)),
                ('ARABIC', models.CharField(max_length=16)),
                ('ARMENIAN', models.CharField(max_length=16)),
                ('BAHASA_INDONESIA', models.CharField(max_length=16)),
                ('BANGLA', models.CharField(max_length=16)),
                ('BULGARIAN', models.CharField(max_length=16)),
                ('CHINESE', models.CharField(max_length=16)),
                ('CZECH', models.CharField(max_length=16)),
                ('DANISH', models.CharField(max_length=16)),
                ('DEUTSCH', models.CharField(max_length=16)),
                ('ESPANOL', models.CharField(max_length=16)),
                ('FARSI', models.CharField(max_length=16)),
                ('FRANCAIS', models.CharField(max_length=16)),
                ('GREEK', models.CharField(max_length=16)),
                ('HEBREW', models.CharField(max_length=16)),
                ('ITALIANO', models.CharField(max_length=16)),
                ('JAPANESE', models.CharField(max_length=16)),
                ('KISWAHILI', models.CharField(max_length=16)),
                ('KOREAN', models.CharField(max_length=16)),
                ('MONGOLIAN', models.CharField(max_length=16)),
                ('NEDERLANDS', models.CharField(max_length=16)),
                ('NEPALI', models.CharField(max_length=16)),
                ('NORSK', models.CharField(max_length=16)),
                ('POLISH', models.CharField(max_length=16)),
                ('PORTUGAL_PORTUGUES', models.CharField(max_length=16)),
                ('PORTUGUES', models.CharField(max_length=16)),
                ('PUNJABI', models.CharField(max_length=16)),
                ('RUSSIAN', models.CharField(max_length=16)),
                ('SERBIAN', models.CharField(max_length=16)),
                ('SINDHI', models.CharField(max_length=16)),
                ('SINHALA', models.CharField(max_length=16)),
                ('TAMIL', models.CharField(max_length=16)),
                ('TELUGU', models.CharField(max_length=16)),
                ('THAI', models.CharField(max_length=16)),
                ('TURKCE', models.CharField(max_length=16)),
                ('UKRAINIAN', models.CharField(max_length=16)),
                ('URDU', models.CharField(max_length=16)),
                ('XHOSA', models.CharField(max_length=16)),
                ('ZULU', models.CharField(max_length=64)),
                ('amaraOK', models.BooleanField(default=False)),
                ('deTranslator', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=32)),
                ('ename', models.CharField(max_length=32)),
                ('master', models.CharField(max_length=32)),
                ('target', models.CharField(max_length=8, choices=[(b'Test', b'Testsite'), (b'Live', b'Livesite'), (b'Rockstar', b'Rockstar')])),
                ('cID', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
