# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haproxygui', '0008_auto_20150605_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='backendserveroption',
            name='backup',
            field=models.BooleanField(default=False),
        ),
    ]
