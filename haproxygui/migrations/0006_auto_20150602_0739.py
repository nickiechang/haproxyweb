# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haproxygui', '0005_default_option_persist'),
    ]

    operations = [
        migrations.AddField(
            model_name='backendserveroption',
            name='weight',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='backendserver',
            name='maxconn',
            field=models.IntegerField(default=2000),
        ),
        migrations.AlterField(
            model_name='backendserveroption',
            name='check',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='backendserveroption',
            name='check_fall',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='backendserveroption',
            name='check_inter',
            field=models.CharField(default=b'2s', max_length=16),
        ),
    ]
