'''
Created on May 13, 2015

@author: nick
'''

from django.core.files import File
from haproxygui.models import *

import os
import shutil
import subprocess
from django.http import HttpResponse
from django.template.response import TemplateResponse

tab1='    '
tab2='        '
tab3='            '

class WriteConfigMiddleware(object):
    def process_template_response(self, request, response):
        #response.context_data["message"] = "message"
        return response
        
    def process_response(self, request, response):
        if request.method == 'POST':
            write_haproxycfg()
            try:
                subprocess.check_output("sudo service haproxy reload 2>&1", shell=True)
            except  subprocess.CalledProcessError as e:
                return TemplateResponse(request, 'error.html', { "errmsg" : e.output}).render()
                #return HttpResponse(e.output)
        return response

def write_haproxycfg():
    os.system("[ -f /tmp/haproxy.cfg ] && sudo chmod 666 /tmp/haproxy.cfg")
    with open('/tmp/haproxy.cfg', 'w') as f:
        cfgfile = File(f)

        cfgfile.write('global' + os.linesep)
        cfgfile.write(tab1 + 'log /dev/log local0' + os.linesep)
        cfgfile.write(tab1 + 'log /dev/log local1 notice' + os.linesep)
        cfgfile.write(tab1 + 'chroot /var/lib/haproxy' + os.linesep)
        cfgfile.write(tab1 + 'stats socket /run/haproxy/admin.sock mode 660 level admin' + os.linesep)
        cfgfile.write(tab1 + 'stats timeout 30s' + os.linesep)
        cfgfile.write(tab1 + 'user haproxy' + os.linesep)
        cfgfile.write(tab1 + 'group haproxy' + os.linesep)
        cfgfile.write(tab1 + 'daemon' + os.linesep)
        cfgfile.write(tab1 + '# Default SSL material locations' + os.linesep)
        cfgfile.write(tab1 + 'ca-base /etc/ssl/certs' + os.linesep)
        cfgfile.write(tab1 + 'crt-base /etc/ssl/private' + os.linesep)
        cfgfile.write(tab1 + '# Default ciphers to use on SSL-enabled listening sockets.' + os.linesep)
        cfgfile.write(tab1 + '# For more information, see ciphers(1SSL).' + os.linesep)
        cfgfile.write(tab1 + 'ssl-default-bind-ciphers kEECDH+aRSA+AES:kRSA+AES:+AES256:RC4-SHA:!kEDH:!LOW:!EXP:!MD5:!aNULL:!eNULL' + os.linesep)

        rows = Default.objects.all()
        cfgfile.write('defaults' + os.linesep)
        for d in rows:
            cfgfile.write(tab1 + 'log       global' + os.linesep)
            cfgfile.write(tab1 + 'option    ' + d.option_log + os.linesep)
            cfgfile.write(tab1 + 'option    dontlognull' + os.linesep)
            cfgfile.write(tab1 + 'maxconn ' + str(d.maxconn) + os.linesep)
            cfgfile.write(tab1 + 'retries ' + str(d.retries) + os.linesep)
            cfgfile.write(tab1 + 'timeout connect ' + d.timeout_connect + os.linesep)
            cfgfile.write(tab1 + 'timeout client ' + d.timeout_client + os.linesep)
            cfgfile.write(tab1 + 'timeout server ' + d.timeout_server + os.linesep)
            cfgfile.write(tab1 + 'timeout http-request ' + d.timeout_server + os.linesep)
            if d.option_redispatch:
                cfgfile.write(tab1 + 'option redispatch' + os.linesep)       
            if d.option_persist:
                cfgfile.write(tab1 + 'option persist' + os.linesep)       
            if d.option_httpclose:
                cfgfile.write(tab1 + 'option httpclose' + os.linesep)       
            cfgfile.write(tab1 + 'errorfile 400 /etc/haproxy/errors/400.http' + os.linesep)
            cfgfile.write(tab1 + 'errorfile 403 /etc/haproxy/errors/403.http' + os.linesep)
            cfgfile.write(tab1 + 'errorfile 408 /etc/haproxy/errors/408.http' + os.linesep)
            cfgfile.write(tab1 + 'errorfile 500 /etc/haproxy/errors/500.http' + os.linesep)
            cfgfile.write(tab1 + 'errorfile 502 /etc/haproxy/errors/502.http' + os.linesep)
            cfgfile.write(tab1 + 'errorfile 503 /etc/haproxy/errors/503.http' + os.linesep)
            cfgfile.write(tab1 + 'errorfile 504 /etc/haproxy/errors/504.http' + os.linesep)

        rows = Frontend.objects.all()
        for r in rows:
            cfgfile.write('frontend ' + r.name + os.linesep)
            if r.mode:
                cfgfile.write(tab1 + 'mode ' + r.mode + os.linesep)
            for b in r.frontend_bind.all():
                cfgfile.write(tab1 + 'bind ' + b.bind_address + ":" + str(b.bind_port))
                if b.sslfile:
                    cfgfile.write(' ssl crt /etc/pki/CA/' + b.sslfile.name)
#                if b.crt_name:
#                    cfgfile.write(' ssl crt /etc/pki/CA/' + b.crt_name)
#           cfgfile.write(tab1 + 'bind ' + r.bind_address + ":" + str(r.bind_port))
#           if r.bind_option:
#               cfgfile.write(' ssl crt /etc/pki/CA/' + r.bind_option.crt_name)
                if b.no_sslv3:
                    cfgfile.write(' no-sslv3')
                if b.force_tls:
                    cfgfile.write(' ' + b.force_tls)
                cfgfile.write(os.linesep)
            if r.maxconn:
                cfgfile.write(tab1 + 'maxconn ' + str(r.maxconn) + os.linesep)
            if hasattr(r, 'default_backend') == True:
                if r.default_backend:
                    cfgfile.write(tab1 + 'default_backend ' + r.default_backend.name + os.linesep)

        rows = Backend.objects.all()
        for b in rows:
            cfgfile.write('backend ' + b.name + os.linesep)
            if b.balance_method != '':
                cfgfile.write(tab1 + 'balance ' + b.balance_method + os.linesep)
            if b.mode:
                cfgfile.write(tab1 + 'mode ' + b.mode + os.linesep)
            if b.forwardfor:
                cfgfile.write(tab1 + 'option forwardfor')
                if b.forwardfor_expect != '':
                    cfgfile.write(' except ' + b.forwardfor_expect)
                if b.forwardfor_header != '':
                    cfgfile.write(' header ' + b.forwardfor_header)
                cfgfile.write(os.linesep)
            if b.cookie:
                cfgfile.write(tab1 + 'cookie ' + b.cookie_name)
                if b.cookie_option_indirect:
                    cfgfile.write(' indirect')
                if b.cookie_option_nocache:
                    cfgfile.write(' nocache')
                if b.cookie_option_postonly:
                    cfgfile.write(' postonly')
                cfgfile.write(os.linesep)
#            if b.backend_check:
            if hasattr(b, 'backend_check') == True:
                if b.backend_check.timeout_check != '':
                    cfgfile.write(tab1 + 'timeout check ' + b.backend_check.timeout_check + os.linesep) 
                if b.backend_check.ssl_hello_check:
                    cfgfile.write(tab1 + 'option ssl-hello-chk' + os.linesep) 
                if b.backend_check.http_check:
                    cfgfile.write(tab1 + 'option httpchk') 
                    if b.backend_check.http_url != '': 
                        cfgfile.write(' ' + b.backend_check.http_method + ' ' + b.backend_check.http_url)
                    cfgfile.write(os.linesep) 
                if b.backend_check.http_check_expect:
                    cfgfile.write(tab1 + 'http-check expect')
                    if b.backend_check.http_check_expect_not: 
                        cfgfile.write(' !')
                    cfgfile.write(' ' + b.backend_check.http_check_expect + ' ' + b.backend_check.http_check_expect_value)
                    cfgfile.write(os.linesep)
                if b.backend_check.disable_on_404: 
                    cfgfile.write(tab1 + 'http-check disable-on-404' + os.linesep)
            for s in BackendServerOption.objects.filter(backend_id=b.name):
                cfgfile.write(tab1 + 'server ' + s.name + ' ' + s.address + ':' + str(s.port))
                if s.check:
                    cfgfile.write(' check inter ' + s.check_inter + ' fall ' + str(s.check_fall))
                if s.cookie_value != '':
                    cfgfile.write(' cookie ' + s.cookie_value)
#                for so in s.server_option.all():
#                    if so.check:
#                        cfgfile.write(' check inter ' + so.check_inter + ' fall ' + str(so.check_fall))
#                    if so.cookie_value != '':
#                        cfgfile.write(' cookie ' + so.cookie_value)
                if s.maxconn:
                    cfgfile.write(' weight ' + str(s.weight))
                if s.maxconn:
                    cfgfile.write(' maxconn ' + str(s.maxconn))
                cfgfile.write(os.linesep)

        cfgfile.write('listen stats :8888' + os.linesep)            
        cfgfile.write('    mode http' + os.linesep)
        cfgfile.write('    stats enable' + os.linesep)
        cfgfile.write('    stats hide-version' + os.linesep)
        cfgfile.write('    stats realm Haproxy\ Statistics' + os.linesep)
        cfgfile.write('    stats uri /' + os.linesep)
        cfgfile.write('    #stats auth your_username:your_password' + os.linesep)
        cfgfile.write('    stats refresh 10s' + os.linesep)
    os.system("sudo cp /tmp/haproxy.cfg /etc/haproxy/haproxy.cfg") 

