from django.db import models
import os

class Default(models.Model):
    choices_option_log = (
        ('tcplog', 'tcp'),
        ('httplog', 'http'),
    )    
    id = models.IntegerField(primary_key=True)
    maxconn = models.IntegerField(default=2000)
    timeout_connect = models.CharField(max_length=16, default='5s')
    timeout_client = models.CharField(max_length=16, default='30s')
    timeout_server = models.CharField(max_length=16, default='30s')
    timeout_http_request = models.CharField(max_length=16, default='10s')
    retries = models.IntegerField(default=3)
    option_redispatch = models.BooleanField(default=True)
    option_persist = models.BooleanField(default=False)
    option_httpclose = models.BooleanField(default=False)
    option_log = models.CharField(max_length=16,choices=choices_option_log, default='tcplog')
    
    class Meta:
        db_table = 'defaultconfig'
 
class Backend(models.Model):
    choices_balance_method = (
        ('source', 'source'),
#        ('first', 'first'),
#        ('static-rr', 'static-rr'),
        ('leastconn', 'leastconn'),
        ('roundrobin', 'roundrobin'),
    )    
    choices_mode = (
        ('tcp', 'tcp'),
        ('http', 'http'),
    )    
    choices_cookie = (
        ('prefix', 'prefix'),
        ('rewrite', 'rewrite'),
        ('insert', 'insert'),
    )    
    name = models.CharField(max_length=255, primary_key=True)
    balance_method = models.CharField(max_length=16,choices=choices_balance_method,default='roundrobin')
    mode = models.CharField(max_length=4,choices=choices_mode, default='http')
    forwardfor = models.BooleanField(default=True)
    forwardfor_expect = models.CharField(max_length=255, default='127.0.0.0/8', blank=True, null=True)
    forwardfor_header = models.CharField(max_length=255, blank=True, null=True)
    cookie = models.CharField(max_length=16,choices=choices_cookie, blank=True, null=True)
    cookie_name = models.CharField(max_length=255, blank=True, null=True)
    cookie_option_indirect = models.BooleanField(default=False)
    cookie_option_nocache = models.BooleanField(default=False)
    cookie_option_postonly = models.BooleanField(default=False)
    cookie_domain = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'backend'

class BackendCheck(Backend):
    choices_http_method = (
        ('OPTIONS', 'OPTIONS'),
        ('HEAD', 'HEAD'),
        ('POST', 'POST'),
        ('GET', 'GET'),
    )        
    choices_http_check_expect = (
        ('rstring', 'rstring'),
        ('string', 'string'),
        ('rstatus', 'rstatus'),
        ('status', 'status'),
    )        
    backend_name = models.OneToOneField(Backend, primary_key=True, db_column='backend_name', to_field='name', related_name='backend_check',parent_link=True)
    ssl_hello_check = models.BooleanField(default=False)
    http_check = models.BooleanField(default=False)
    http_method = models.CharField(max_length=16,choices=choices_http_method, default='GET')
    http_url = models.CharField(max_length=255, default='/')
    http_check_expect = models.CharField(max_length=16,choices=choices_http_check_expect, default='', blank=True, null=True)
    http_check_expect_not = models.BooleanField(default=False)
    http_check_expect_value = models.CharField(max_length=255, default='200', blank=True, null=True)
    disable_on_404 = models.BooleanField(default=False)
    timeout_check = models.CharField(max_length=16, default='5s', blank=True, null=True)       

    class Meta:
        db_table = 'backend_check'

class BackendServer(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    address = models.CharField(max_length=255)
    port = models.IntegerField()
    weight = models.IntegerField(default=1)
    maxconn = models.IntegerField(default=2000)
    backend = models.ForeignKey(Backend,db_column='backend_name', to_field='name', related_name='backend_server')

    class Meta:
        db_table = 'backend_server'

class ServerOption(models.Model):
    backend_server = models.OneToOneField(BackendServer, primary_key=True, db_column='backend_server_name', to_field='name', related_name='server_option')
#    backend_server_name = models.OneToOneField(BackendServer, primary_key=True, db_column='backend_server_name', to_field='name', related_name='server_option',parent_link=True)
    check = models.BooleanField()
    check_inter = models.CharField(max_length=16)
    check_fall = models.IntegerField()
    cookie_value = models.CharField(max_length=16)

    class Meta:
        db_table = 'server_option'

class BackendServerOption(BackendServer):
    backend_server_name = models.OneToOneField(BackendServer, primary_key=True, db_column='backend_server_name', to_field='name', related_name='backend_server_option',parent_link=True)
    check = models.BooleanField(default=False)
    check_inter = models.CharField(max_length=16,default='2s')
    check_fall = models.IntegerField(default=3)
    cookie_value = models.CharField(max_length=16)

    class Meta:
        db_table = 'backend_server_option'
            
class Frontend(models.Model):
    choices_mode = (
        ('tcp', 'tcp'),
        ('http', 'http'),
    )
    name = models.CharField(max_length=255, primary_key=True)
    default_backend = models.ForeignKey(Backend, db_column='default_backend', to_field='name', related_name='frontend', blank=True, null=True)
    mode = models.CharField(max_length=16,choices=choices_mode, blank=False, default='http')
    maxconn = models.IntegerField(default=2000)
#    bind_address = models.GenericIPAddressField(max_length=32)
#    bind_port = models.IntegerField()
#    default_backend = models.CharField(max_length=255, blank=True, null=True)
#    use_ssl = models.BooleanField()

    class Meta:
        db_table = 'frontend'

def get_path_and_name(instance, filename): 
    new_name = instance.name 
    return new_name

class SSLFile(models.Model):
    name = models.CharField(max_length=255)
    sslfile = models.FileField(upload_to=get_path_and_name)

    def delete(self,*args,**kwargs):
        if os.path.isfile(self.sslfile.path):
            os.remove(self.sslfile.path)

        super(SSLFile, self).delete(*args,**kwargs)
        
    class Meta:
        db_table = 'sslfile'
        
class FrontendBind(models.Model):
    choices_force_tls = (
        ('force-tlsv10', 'v10'),
        ('force-tlsv11', 'v11'),
        ('force-tlsv12', 'v12'),
    )
    frontend = models.ForeignKey(Frontend, db_column='frontend_name', to_field='name', related_name='frontend_bind')
    bind_address = models.CharField(max_length=255)
    bind_port = models.IntegerField()
    sslfile = models.ForeignKey(SSLFile, related_name='frontend_bind', blank=True, null=True)
    no_sslv3 = models.BooleanField(default=True)
    force_tls = models.CharField(max_length=16,choices=choices_force_tls, blank=True, null=True)
#    crt_name = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'frontend_bind'

    
class BindOption(Frontend):
    frontend_name = models.OneToOneField(Frontend, primary_key=True, db_column='frontend_name', to_field='name', related_name='bind_option',parent_link=True)
#    frontend_name = models.ForeignKey(Frontend, primary_key=True, db_column='frontend_name', to_field='name', related_name='bind_option',unique=True)
    crt_name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'bind_option'


