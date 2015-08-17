'''
Created on May 18, 2015

@author: nick
'''
from haproxygui.models import *
from django.views.generic import ListView,DetailView

from myforms import *
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy,reverse
from django.shortcuts import get_object_or_404

class SSLFileList(ListView):
    model = SSLFile
    template_name = 'sslfile_list.html'

class SSLFileCreate(CreateView):
    model = SSLFile
    form_class = SSLFileForm
    template_name = 'sslfile_detail.html'
    def get_success_url(self):
        return reverse('sslfile_list')    

class SSLFileDelete(DeleteView):
    model = SSLFile
    template_name = 'sslfile_confirm_delete.html'
    def get_success_url(self):
        return reverse('sslfile_list')    
    
class FrontendList(ListView):
    model = Frontend
    template_name = 'frontend_list.html'

class FrontendCreate(CreateView):
    model = Frontend
    form_class = FrontendForm
    template_name = 'frontend_update.html'
    def get_success_url(self):
        return reverse('frontend_list')    

class FrontendDelete(DeleteView):
    model = Frontend
    template_name = 'frontend_confirm_delete.html'
    def get_success_url(self):
        return reverse('frontend_list')    
    
class FrontendUpdate(SuccessMessageMixin,UpdateView):
    model = Frontend
    #queryset = Frontend.objects.all()
    form_class = FrontendForm
    #fields = ['name','default_backend','mode','maxconn','use_ssl']
    template_name = 'frontend_update.html'
    #success_url = reverse_lazy('frontend_updateview')
    success_message = "Update Successfully"

    def get_form(self, form_class):
        form = super(FrontendUpdate, self).get_form(form_class)
        form.fields['name'].widget.attrs['readonly']=True
        return form
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FrontendUpdate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['bind_option'] = BindOption.objects.all()
        return context
    def get_success_url(self):
        return reverse('frontend_update', kwargs={'pk': self.object.pk})    

class FrontendBindList(ListView):
    model = FrontendBind
    template_name = 'frontend_bind_list.html'
    #queryset = FrontendBind.objects.filter(frontend__name='http1')
    #context_object_name = 'frontend_bind_list'
    def get_queryset(self):
        self.frontend = get_object_or_404(Frontend, name=self.kwargs['frontend_name'])
        return FrontendBind.objects.filter(frontend=self.frontend)
        #return FrontendBind.objects.filter(frontend__name=self.kwargs['frontend_name'])
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FrontendBindList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['fronetendbind'] = self.fronetendbind
        #context['bind_option'] = BindOption.objects.all()
        context['frontend_name'] = self.kwargs['frontend_name']
        return context

class FrontendBindCreate(CreateView):
    model = FrontendBind
    #fields = ['frontend', 'bind_address', 'bind_port', 'crt_name']
    form_class = FrontendBindForm
    template_name = 'frontend_bind_update.html'
    def get_initial(self):
        initial = super(FrontendBindCreate, self).get_initial()
        initial = initial.copy()
        initial['frontend'] = self.kwargs['frontend_name']
        return initial

    def get_success_url(self):
        return reverse('frontend_bind_list', kwargs={'frontend_name': self.object.frontend_id})    

class FrontendBindDelete(DeleteView):
    model = FrontendBind
    template_name = 'frontend_bind_confirm_delete.html'
    def get_success_url(self):
        return reverse('frontend_bind_list', kwargs={'frontend_name': self.object.frontend_id})    
    
class FrontendBindUpdate(SuccessMessageMixin, UpdateView):
    model = FrontendBind
    #queryset = FrontendBind.objects.filter(frontend__name=self.args[0])
    form_class = FrontendBindForm
    #fields = ['name','default_backend','mode','maxconn','use_ssl']
    template_name = 'frontend_bind_update.html'
    #success_url = reverse_lazy('frontend_updateview')
    success_message = "Update Successfully"

    def get_success_url(self):
        return reverse('frontend_bind_update', kwargs={'pk': self.object.pk})    

class BackendList(ListView):
    model =BackendCheck
    template_name = 'backend_list.html'

class BackendCreate(CreateView):
    model = BackendCheck
    form_class = BackendCheckForm
    template_name = 'backend_update.html'
    def get_success_url(self):
        return reverse('backend_list')    

class BackendUpdate(SuccessMessageMixin, UpdateView):
    model = BackendCheck
    form_class = BackendCheckForm
    template_name = 'backend_update.html'
    success_message = "Update Successfully"
    
    def get_form(self, form_class):
        form = super(BackendUpdate, self).get_form(form_class)
        form.fields['name'].widget.attrs['readonly']=True
        return form
    
    def get_context_data(self, **kwargs):
        context = super(BackendUpdate, self).get_context_data(**kwargs)
#        context['status'] = 'Success'
        return context

#    def get_success_message(self, cleaned_data):
#        return self.success_message % dict(cleaned_data, calculated_field=self.object.calculated_field)
    
    def get_success_url(self):
        return reverse('backend_update', kwargs={'pk': self.object.pk})    

class BackendDelete(DeleteView):
    model = BackendCheck
    template_name = 'backend_confirm_delete.html'
    def get_success_url(self):
        return reverse('backend_list')    

class BackendServerList(ListView):
    model =BackendServerOption
    template_name = 'backend_server_list.html'

    def get_queryset(self):
        self.backend = get_object_or_404(Backend, name=self.kwargs['backend_name'])
        return BackendServerOption.objects.filter(backend=self.backend)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BackendServerList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['backend_name'] = self.kwargs['backend_name']
        return context

class BackendServerCreate(CreateView):
    model = BackendServerOption
    form_class = BackendServerOptionForm
    template_name = 'backend_server_update.html'

    def get_initial(self):
        initial = super(BackendServerCreate, self).get_initial()
        initial = initial.copy()
        initial['backend'] = self.kwargs['backend_name']
        return initial

    def get_success_url(self):
        return reverse('backend_server_list', kwargs={'backend_name': self.object.backend_id})    

class BackendServerUpdate(SuccessMessageMixin, UpdateView):
    model = BackendServerOption
    form_class = BackendServerOptionForm
    template_name = 'backend_server_update.html'
    success_message = "Update Successfully"
   
    def get_form(self, form_class):
        form = super(BackendServerUpdate, self).get_form(form_class)
        form.fields['name'].widget.attrs['readonly']=True
        return form
    
    def get_context_data(self, **kwargs):
        context = super(BackendServerUpdate, self).get_context_data(**kwargs)
        return context
    
    def get_success_url(self):
        return reverse('backend_server_update', kwargs={'pk': self.object.pk})    

class BackendServerDelete(DeleteView):
    model = BackendServerOption
    template_name = 'backend_server_confirm_delete.html'
    def get_success_url(self):
        return reverse('backend_server_list', kwargs={'backend_name': self.object.backend_id})    
        
class FrontendView(FormView):
    template_name = 'frontend_list.html'
    form_class = FrontendForm
    success_url = '/frontend/'