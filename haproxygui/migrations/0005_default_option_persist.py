# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haproxygui', '0004_auto_20150602_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='default',
            name='option_persist',
            field=models.BooleanField(default=False),
        ),
    ]
