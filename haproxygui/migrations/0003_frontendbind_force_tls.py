# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haproxygui', '0002_auto_20150602_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontendbind',
            name='force_tls',
            field=models.CharField(max_length=16, null=True, choices=[(b'force-tlsv10', b'force-tlsv10'), (b'force-tlsv11', b'force-tlsv11'), (b'force-tlsv12', b'force-tlsv12')]),
        ),
    ]
