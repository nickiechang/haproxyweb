# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haproxygui', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontendbind',
            name='no_sslv3',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='backend',
            name='forwardfor_expect',
            field=models.CharField(default=b'127.0.0.0/8', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='serveroption',
            name='backend_server',
            field=models.OneToOneField(related_name='server_option', primary_key=True, db_column=b'backend_server_name', serialize=False, to='haproxygui.BackendServer'),
        ),
    ]
