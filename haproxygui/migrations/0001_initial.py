# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connection
import haproxygui.models
from django.contrib.auth.models import User

def check_create_database(apps, schema_editor):
    cursor = connection.cursor()
    if 'haproxy' in connection.introspection.table_names():
        print 'exists'
    else:
        print 'no exists'

def create_root_superuser(apps, schema_editor):
    User.objects.create_superuser('root', 'root@example.com', 'testlab')
    
def add_default_row(apps, schema_editor):
    defaultmodel = apps.get_model("haproxygui", "Default")
    defaultrow = defaultmodel()
    defaultrow.id = 1
    defaultrow.maxconn = 2000
    defaultrow.timeout_connect = '5s'
    defaultrow.timeout_client = '30s'
    defaultrow.timeout_server = '30s'
    defaultrow.timeout_http_request = '10s'
    defaultrow.retries = 3
    defaultrow.option_redispatch = True
    defaultrow.option_persist = False
    defaultrow.option_httpclose = False   
    defaultrow.option_log = 'tcplog'   
    defaultrow.save() 

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        #migrations.RunPython(check_create_database),
        migrations.CreateModel(
            name='Backend',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('balance_method', models.CharField(default=b'roundrobin', max_length=16, choices=[(b'source', b'source'), (b'first', b'first'), (b'static-rr', b'static-rr'), (b'leastconn', b'leastconn'), (b'roundrobin', b'roundrobin')])),
                ('mode', models.CharField(default=b'http', max_length=4, choices=[(b'tcp', b'tcp'), (b'http', b'http')])),
                ('forwardfor', models.BooleanField(default=True)),
                ('forwardfor_expect', models.CharField(default=b'127.0.0.1', max_length=255, null=True, blank=True)),
                ('forwardfor_header', models.CharField(max_length=255, null=True, blank=True)),
                ('cookie', models.CharField(blank=True, max_length=16, null=True, choices=[(b'prefix', b'prefix'), (b'rewrite', b'rewrite'), (b'insert', b'insert')])),
                ('cookie_name', models.CharField(max_length=255, null=True, blank=True)),
                ('cookie_option_indirect', models.BooleanField(default=False)),
                ('cookie_option_nocache', models.BooleanField(default=False)),
                ('cookie_option_postonly', models.BooleanField(default=False)),
                ('cookie_domain', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'backend',
            },
        ),
        migrations.CreateModel(
            name='BackendServer',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('address', models.CharField(max_length=255)),
                ('port', models.IntegerField()),
                ('maxconn', models.IntegerField()),
            ],
            options={
                'db_table': 'backend_server',
            },
        ),
        migrations.CreateModel(
            name='Default',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('maxconn', models.IntegerField(default=2000)),
                ('timeout_connect', models.CharField(default=b'5s', max_length=16)),
                ('timeout_client', models.CharField(default=b'30s', max_length=16)),
                ('timeout_server', models.CharField(default=b'30s', max_length=16)),
                ('retries', models.IntegerField(default=3)),
                ('option_redispatch', models.BooleanField(default=True)),
                ('option_httpclose', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'defaultconfig',
            },
        ),
        migrations.CreateModel(
            name='Frontend',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('mode', models.CharField(default=b'http', max_length=16, choices=[(b'tcp', b'tcp'), (b'http', b'http')])),
                ('maxconn', models.IntegerField(default=2000)),
            ],
            options={
                'db_table': 'frontend',
            },
        ),
        migrations.CreateModel(
            name='FrontendBind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bind_address', models.CharField(max_length=255)),
                ('bind_port', models.IntegerField()),
            ],
            options={
                'db_table': 'frontend_bind',
            },
        ),
        migrations.CreateModel(
            name='SSLFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('sslfile', models.FileField(upload_to=haproxygui.models.get_path_and_name)),
            ],
            options={
                'db_table': 'sslfile',
            },
        ),
        migrations.CreateModel(
            name='BackendCheck',
            fields=[
                ('backend_name', models.OneToOneField(parent_link=True, related_name='backend_check', primary_key=True, db_column=b'backend_name', serialize=False, to='haproxygui.Backend')),
                ('ssl_hello_check', models.BooleanField(default=False)),
                ('http_check', models.BooleanField(default=False)),
                ('http_method', models.CharField(default=b'GET', max_length=16, choices=[(b'OPTIONS', b'OPTIONS'), (b'HEAD', b'HEAD'), (b'POST', b'POST'), (b'GET', b'GET')])),
                ('http_url', models.CharField(default=b'/', max_length=255)),
                ('http_check_expect', models.CharField(default=b'', max_length=16, null=True, blank=True, choices=[(b'rstring', b'rstring'), (b'string', b'string'), (b'rstatus', b'rstatus'), (b'status', b'status')])),
                ('http_check_expect_not', models.BooleanField(default=False)),
                ('http_check_expect_value', models.CharField(default=b'200', max_length=255, null=True, blank=True)),
                ('disable_on_404', models.BooleanField(default=False)),
                ('timeout_check', models.CharField(default=b'5s', max_length=16, null=True, blank=True)),
            ],
            options={
                'db_table': 'backend_check',
            },
            bases=('haproxygui.backend',),
        ),
        migrations.CreateModel(
            name='BackendServerOption',
            fields=[
                ('backend_server_name', models.OneToOneField(parent_link=True, related_name='backend_server_option', primary_key=True, db_column=b'backend_server_name', serialize=False, to='haproxygui.BackendServer')),
                ('check', models.BooleanField()),
                ('check_inter', models.CharField(max_length=16)),
                ('check_fall', models.IntegerField()),
                ('cookie_value', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'backend_server_option',
            },
            bases=('haproxygui.backendserver',),
        ),
        migrations.CreateModel(
            name='BindOption',
            fields=[
                ('frontend_name', models.OneToOneField(parent_link=True, related_name='bind_option', primary_key=True, db_column=b'frontend_name', serialize=False, to='haproxygui.Frontend')),
                ('crt_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'bind_option',
            },
            bases=('haproxygui.frontend',),
        ),
        migrations.CreateModel(
            name='ServerOption',
            fields=[
                ('backend_server', models.ForeignKey(related_name='server_option', primary_key=True, db_column=b'backend_server_name', serialize=False, to='haproxygui.BackendServer')),
                ('check', models.BooleanField()),
                ('check_inter', models.CharField(max_length=16)),
                ('check_fall', models.IntegerField()),
                ('cookie_value', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'server_option',
            },
        ),
        migrations.AddField(
            model_name='frontendbind',
            name='frontend',
            field=models.ForeignKey(related_name='frontend_bind', db_column=b'frontend_name', to='haproxygui.Frontend'),
        ),
        migrations.AddField(
            model_name='frontendbind',
            name='sslfile',
            field=models.ForeignKey(related_name='frontend_bind', blank=True, to='haproxygui.SSLFile', null=True),
        ),
        migrations.AddField(
            model_name='frontend',
            name='default_backend',
            field=models.ForeignKey(related_name='frontend', db_column=b'default_backend', blank=True, to='haproxygui.Backend', null=True),
        ),
        migrations.AddField(
            model_name='backendserver',
            name='backend',
            field=models.ForeignKey(related_name='backend_server', db_column=b'backend_name', to='haproxygui.Backend'),
        ),
        migrations.RunPython(add_default_row),
        migrations.RunPython(create_root_superuser),
    ]
