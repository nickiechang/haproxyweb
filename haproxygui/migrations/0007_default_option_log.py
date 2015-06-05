# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haproxygui', '0006_auto_20150602_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='default',
            name='option_log',
            field=models.CharField(default=b'tcplog', max_length=16, choices=[(b'tcplog', b'tcp'), (b'httplog', b'http')]),
        ),
    ]
