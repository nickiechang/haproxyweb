from django import forms
from haproxygui.models import *
from haproxygui.help import HELP_TEXT

from django.utils.translation import ugettext_lazy as _
from django.forms.fields import Field

class SSLFileForm(forms.ModelForm):
    class Meta:
        model = SSLFile
        fields=('__all__')

        labels = {
            'name': _('File Name'),
            'sslfile': _('Select SSL Certificates File'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'form-control'}),
            'sslfile': forms.FileInput(),
        }


class UploadFileForm(forms.Form):
    file_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    file = forms.FileField(label='Select a file')

class DefaultForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DefaultForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            ': :type field: Field'
            if HELP_TEXT.has_key(field):
                self.fields[field].widget.attrs['title']=HELP_TEXT[field]

    class Meta:
        model = Default
        exclude = ['id']
        
        labels = {
            'maxconn': _('Maximum Connections'),
            'timeout_connect': _('Connection Timeout'),
            'timeout_client': _('Client Timeout'),
            'timeout_server': _('Server Timeout'),
            'timeout_http_request': _('Http Request Timeout'),
            'retries': _('Retries'),
            'option_redispatch': _('Http Redispatch'),
            'option_persist': _('Http Persist'),
            'option_httpclose': _('Force Httpclose'),
            'option_log': _('Log Format'),
        }
        widgets = {
            'maxconn': forms.NumberInput(attrs={'class' : 'form-control'}),
            'timeout_connect': forms.TextInput(attrs={'class' : 'form-control','placeholder': 'ms, s, m, h, d'}),
            'timeout_client': forms.TextInput(attrs={'class' : 'form-control','placeholder': 'ms, s, m, h, d'}),
            'timeout_server': forms.TextInput(attrs={'class' : 'form-control','placeholder': 'ms, s, m, h, d'}),
            'timeout_http_request': forms.TextInput(attrs={'class' : 'form-control','placeholder': 'ms, s, m, h, d'}),
            'retries': forms.NumberInput(attrs={'class' : 'form-control'}),
            'option_redispatch': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'option_persist': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'option_httpclose': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'option_log': forms.Select(attrs={'class' : 'form-control'}),
        }

class FrontendForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FrontendForm, self).__init__(*args, **kwargs)
        self.fields['default_backend'].label_from_instance = lambda obj:obj.name
        for field in self.fields:
            ': :type field: Field'
            if HELP_TEXT.has_key(field):
                self.fields[field].widget.attrs['title']=HELP_TEXT[field]

    class Meta:
        model = Frontend
        fields=('__all__')
        
        labels = {
            'name': _('Name'),
#            'bind_address': _('Bind Address'),
#            'bind_port': _('Bind Port'),
            'default_backend': _('Default Backend'),
            'mode': _('Mode'),
            'maxconn': _('Maximum Connecitons'),
#            'use_ssl': _('Use SSL Certificates'),
#            'crt_name': _('SSL Certificates File Name'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'form-control'}),
#            'bind_address': forms.TextInput(attrs={'class' : 'form-control'}),
#            'bind_port': forms.NumberInput(attrs={'class' : 'form-control'}),
            'default_backend': forms.Select(attrs={'class' : 'form-control'}),
            'mode': forms.Select(attrs={'class' : 'form-control'}),
            'maxconn': forms.NumberInput(attrs={'class' : 'form-control'}),
#            'use_ssl': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
#            'crt_name': forms.TextInput(attrs={'class' : 'form-control'}),
        }

class FrontendBindForm(forms.ModelForm):
    #frontend=forms.MultipleChoiceField(Frontend.objects.all(),label='Frontend Name',widget=forms.Select(attrs={'class' : 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(FrontendBindForm, self).__init__(*args, **kwargs)
        self.fields['sslfile'].label_from_instance = lambda obj:obj.name
        for field in self.fields:
            ': :type field: Field'
            if HELP_TEXT.has_key(field):
                self.fields[field].widget.attrs['title']=HELP_TEXT[field]
#        self.fields['frontend'].empty_label=None
#        self.fields['frontend'].label_from_instance = lambda obj:obj.name
         
    class Meta:
        model = FrontendBind
        fields=('__all__')
        
        labels = {
            'frontend': _('Frontend Name'),
            'bind_address': _('Bind Address'),
            'bind_port': _('Bind Port'),
            'sslfile': _('SSL Certificates File Name'),
            'no_sslv3': _('Disable SSLv3'),
            'force_tls': _('Force TLS'),
#            'crt_name': _('SSL Certificates File Name'),
        }
        widgets = {
            'frontend': forms.TextInput(attrs={'class' : 'form-control', 'readonly' :True}),
#            'frontend': forms.Select(attrs={'class' : 'form-control'}),
            'bind_address': forms.TextInput(attrs={'class' : 'form-control','placeholder': '* , 0.0.0.0 , 127.0.0.1 , 192.168.1.1 ...'}),
            'bind_port': forms.NumberInput(attrs={'class' : 'form-control'}),
#            'crt_name': forms.TextInput(attrs={'class' : 'form-control'}),
            'sslfile': forms.Select(attrs={'class' : 'form-control'}),
            'no_sslv3': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'force_tls': forms.Select(attrs={'class' : 'form-control'}),
        }
        
class BindOptionForm(forms.ModelForm):
    class Meta:
        model = BindOption
        exclude = ['frontend_name']
        
        labels = {
            'name': _('Name'),
            'bind_address': _('Bind Address'),
            'bind_port': _('Bind Port'),
            'default_backend': _('Default Backend'),
            'mode': _('Mode'),
            'maxconn': _('Max Conneciton'),
            'use_ssl': _('Use SSL Certificates'),
            'crt_name': _('SSL Certificates File Name'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'form-control'}),
            'bind_address': forms.TextInput(attrs={'class' : 'form-control'}),
            'bind_port': forms.NumberInput(attrs={'class' : 'form-control'}),
            'default_backend': forms.TextInput(attrs={'class' : 'form-control'}),
            'mode': forms.Select(attrs={'class' : 'form-control'}),
            'maxconn': forms.NumberInput(attrs={'class' : 'form-control'}),
            'use_ssl': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'crt_name': forms.TextInput(attrs={'class' : 'form-control'}),
        }

class BackendForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BackendForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            ': :type field: Field'
            if HELP_TEXT.has_key(field):
                self.fields[field].widget.attrs['title']=HELP_TEXT[field]

    class Meta:
        model = Backend
        fields=('__all__')
        
        labels = {
            'name': _('Name'),
            'balance_method': _('Balance Mode'),
            'mode': _('Mode'),
            'forwardfor': _('Forwardfor'),
            'forwardfor_expect': _('Forwardfor Expect'),
            'forwardfor_header': _('Forwardfor Header'),
            'cookie': _('Cookie'),
            'cookie_name': _('Cookie Name'),
            'cookie_option_indirect': _('Cookie Option Indirect'),
            'cookie_option_nocache': _('Cookie Option Nocache'),
            'cookie_option_postonly': _('Cookie Option Postonly'),
            'cookie_domain': _('Cookie Domain'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'form-control'}),
            'balance_method': forms.Select(attrs={'class' : 'form-control'}),
            'mode': forms.Select(attrs={'class' : 'form-control'}),
            'forwardfor': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'forwardfor_expect': forms.TextInput(attrs={'class' : 'form-control'}),
            'forwardfor_header': forms.TextInput(attrs={'class' : 'form-control'}),
            'cookie': forms.Select(attrs={'class' : 'form-control'}),
            'cookie_name': forms.TextInput(attrs={'class' : 'form-control'}),
            'cookie_option_indirect': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'cookie_option_nocache': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'cookie_option_postonly': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'cookie_domain': forms.TextInput(attrs={'class' : 'form-control'}),
        }

class BackendCheckForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BackendCheckForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            ': :type field: Field'
            if HELP_TEXT.has_key(field):
                self.fields[field].widget.attrs['title']=HELP_TEXT[field]

    class Meta:
        model = BackendCheck
        exclude = ['backend_name']
        
        labels = {
            'name': _('Name'),
            'balance_method': _('Balance Mode'),
            'mode': _('Mode'),
            'forwardfor': _('Add X-Forwarded-For'),
            'forwardfor_expect': _('X-Forwarded-For Expect'),
            'forwardfor_header': _('X-Forwarded-For Header'),
            'cookie': _('Cookie'),
            'cookie_name': _('Cookie Name'),
            'cookie_option_indirect': _('Cookie Option Indirect'),
            'cookie_option_nocache': _('Cookie Option Nocache'),
            'cookie_option_postonly': _('Cookie Option Postonly'),
            'cookie_domain': _('Cookie Domain'),
            'ssl_hello_check': _('Https SSL Hello Check'),
            'http_check': _('Http Check'),
            'http_method': _('Http Method'),
            'http_url': _('Http Url'),
            'http_check_expect': _('Http Check Expect'),
            'http_check_expect_not': _('Http Check Expect Not'),
            'http_check_expect_value': _('Http Check Expect Value'),
            'disable_on_404': _('Disable on 404'),
            'timeout_check': _('Check Timeout'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'form-control'}),
            'balance_method': forms.Select(attrs={'class' : 'form-control'}),
            'mode': forms.Select(attrs={'class' : 'form-control'}),
            'forwardfor': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'forwardfor_expect': forms.TextInput(attrs={'class' : 'form-control'}),
            'forwardfor_header': forms.TextInput(attrs={'class' : 'form-control'}),
            'cookie': forms.Select(attrs={'class' : 'form-control'}),
            'cookie_name': forms.TextInput(attrs={'class' : 'form-control'}),
            'cookie_option_indirect': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'cookie_option_nocache': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'cookie_option_postonly': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'cookie_domain': forms.TextInput(attrs={'class' : 'form-control'}),
            'ssl_hello_check': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'http_check': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'http_method': forms.Select(attrs={'class' : 'form-control'}),
            'http_url': forms.TextInput(attrs={'class' : 'form-control'}),
            'http_check_expect': forms.Select(attrs={'class' : 'form-control'}),
            'http_check_expect_not': forms.RadioSelect(choices=[(True, 'is not'),(False, 'is')]),
            'http_check_expect_value': forms.TextInput(attrs={'class' : 'form-control'}),
            'disable_on_404': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'timeout_check': forms.TextInput(attrs={'class' : 'form-control','placeholder': 'ms, s, m, h, d'}),
        }

class BackendServerForm(forms.ModelForm):
    class Meta:
        model = BackendServer
        fields=('__all__')

class ServerDetailForm(forms.Form):
    name=forms.CharField(label='Name',max_length=255,widget=forms.TextInput(attrs={'class' : 'form-control'}))
#    backend_name=forms.CharField(label='Backend Name',max_length=255,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    address=forms.CharField(label='Address',max_length=32,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    port=forms.IntegerField(label='Port',widget=forms.TextInput(attrs={'class' : 'form-control'}))
    maxconn=forms.IntegerField(label='Max Connection',widget=forms.TextInput(attrs={'class' : 'form-control'}))
#    backend_server_name=forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    #check=forms.BooleanField(label='Check',widget=forms.CheckboxInput(attrs={'class' : 'checkbox'}))
    check=forms.BooleanField(widget=forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]))
    #check=forms.TypedChoiceField(coerce=lambda x: bool(int(x)),
    #               choices=((0, 'False'), (1, 'True')),
    #               widget=forms.RadioSelect
    #            )
    check_inter=forms.CharField(label='Check Inter',max_length=16,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    check_fall=forms.IntegerField(label='Check Fall',widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    cookie_value=forms.CharField(label='Cookie Value',max_length=255,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    
class BackendServerOptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BackendServerOptionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            ': :type field: Field'
            if HELP_TEXT.has_key(field):
                self.fields[field].widget.attrs['title']=HELP_TEXT[field]

    class Meta:
        model = BackendServerOption
        exclude = [ 'backend_server_name']

        labels = {
            'name': _('Name'),
            'address': _('Address'),
            'port': _('Post'),
            'maxconn': _('Maximum Connections'),
            'weight': _('Weight'),
            'check': _('Check'),
            'check_inter': _('Check Interval'),
            'check_fall': _('Check Fall'),
            'cookie_value': _('Cookie Value'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'form-control'}),
            'address': forms.TextInput(attrs={'class' : 'form-control'}),
            'port': forms.NumberInput(attrs={'class' : 'form-control'}),
            'maxconn': forms.NumberInput(attrs={'class' : 'form-control'}),
            'weight': forms.NumberInput(attrs={'class' : 'form-control'}),
            'check': forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]),
            'check_inter': forms.TextInput(attrs={'class' : 'form-control'}),
            'check_fall': forms.NumberInput(attrs={'class' : 'form-control'}),
            'cookie_value': forms.TextInput(attrs={'class' : 'form-control'}),
            'backend': forms.HiddenInput(),
        }
