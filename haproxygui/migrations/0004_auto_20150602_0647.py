# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haproxygui', '0003_frontendbind_force_tls'),
    ]

    operations = [
        migrations.AddField(
            model_name='default',
            name='timeout_http_request',
            field=models.CharField(default=b'10s', max_length=16),
        ),
        migrations.AlterField(
            model_name='frontendbind',
            name='force_tls',
            field=models.CharField(blank=True, max_length=16, null=True, choices=[(b'force-tlsv10', b'v10'), (b'force-tlsv11', b'v11'), (b'force-tlsv12', b'v12')]),
        ),
    ]
