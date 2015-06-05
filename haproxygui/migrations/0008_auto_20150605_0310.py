# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haproxygui', '0007_default_option_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backendserveroption',
            name='weight',
        ),
        migrations.AddField(
            model_name='backendserver',
            name='weight',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='backend',
            name='balance_method',
            field=models.CharField(default=b'roundrobin', max_length=16, choices=[(b'source', b'source'), (b'leastconn', b'leastconn'), (b'roundrobin', b'roundrobin')]),
        ),
    ]
