from django.shortcuts import render, render_to_response, redirect,get_object_or_404,get_list_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory, inlineformset_factory
from django.conf import settings

from haproxygui.models import *
from myforms import *
from files import *

import os
import logging
from django.core.exceptions import ObjectDoesNotExist
logger = logging.getLogger(__name__)

def dummy(request):
    ':type request: HttpRequest'
    ':rtype HttpResponse'
    try:
        d = Default.objects.get(id=1) 
        ': :type d: Default'
    except ObjectDoesNotExist:
        Default.objects.create(id=1,maxconn=2000,timeout_connect='5s',timeout_client='30s',timeout_server='30s',retries=3, option_redispatch=1, option_httpclose=0)
    write_haproxycfg()
    return render_to_response('base.html', context_instance=RequestContext(request))

@login_required
def status(request):
#    return render_to_response('status.html',{ 'host': settings.DATABASES['default']['HOST'] }, context_instance=RequestContext(request))
    haproxyurl = request.get_host().replace(":8000", ":8888")
    print haproxyurl
    return render(request, 'status.html',{ 'haproxyhost': haproxyurl })
    #return render(request, 'status.html',{ 'haproxyhost': settings.HAPROXY_URL })

def login(request):
    if request.method == 'POST':
        uname = request.POST.get('username', '')
        psword = request.POST.get('password', '')
        nxt = request.POST.get('next', '')
        user = auth.authenticate(username=uname, password=psword)
        # if the user logs in and is active
        if user is not None and user.is_active:
            auth.login(request, user)
            if nxt:
                return redirect(nxt)
            #return redirect("../../status/") 
            return redirect('home')
        else:
            return render_to_response('login.html', {'login_failed': '1',}, context_instance=RequestContext(request))
    else:
        initialData = {'login_failed': '0'}
        context_instance = RequestContext(request, initialData)
        return render_to_response('login.html', {'next':request.GET.get('next','')}, context_instance)
        #return render(request,'login.html')  

def logout(request):
    auth.logout(request)
    return redirect('login')    

def theme(request):
    return render_to_response('development/theme.html')
    #return render(request,'theme.html')

@login_required
def default(request):
    #return HttpResponse("You're voting on question")
    #rows = Default.objects.all()
    #return render(request,'development/default.html',{'rows': rows})
    logger.debug("Test")
    defaultmodel = get_object_or_404(Default,id=1)
    logger.debug(defaultmodel.timeout_connect)
    form = DefaultForm(request.POST or None, instance=defaultmodel)
    if form.is_valid():
        defaultmodel = form.save()
        logger.debug(defaultmodel.timeout_connect)
        return render(request,'default.html',{'form': form})
    return render(request,'default.html',{'form': form})

@login_required
def frontend(request):
    #FrontendFormset = modelformset_factory(Frontend, fields=('name','bind_address','bind_port','mode'),extra=0)
    #formset = FrontendFormset(queryset=Frontend.objects.all())
    #return render(request,'development/model_frontend.html',{'formset': formset})
    rows = Frontend.objects.select_related().all()
    return render(request,'development/frontend.html',{'rows': rows})

@login_required
def frontend_detail(request, frontend_name):
    bindoptionmodel = get_object_or_404(BindOption,frontend_name=frontend_name)
    form = BindOptionForm(request.POST or None, instance=bindoptionmodel)
    if form.is_valid():
        bindoptionmodel = form.save()
        return render(request,'development/model_frontend_detail.html',{'form': form, 'frontend_name': frontend_name})
    return render(request,'development/model_frontend_detail.html',{'form': form, 'frontend_name': frontend_name})

@login_required
def action_frontend_detail(request, action, frontend_name):
    if request.method == 'POST':
        if action == 'add':
            form = BindOptionForm(request.POST or None)
            if form.is_valid():
                bindoptionmodel = form.save()
            return redirect("frontend")
    else:
        if action == 'delete':
            bindoptionmodel = get_object_or_404(BindOption,frontend_name=frontend_name)
            bindoptionmodel.delete()
            return redirect("frontend")
        form = BindOptionForm()  
    return render(request,'development/model_frontend_detail.html',{'form': form})

@login_required
def backend(request):
    rows = Backend.objects.select_related().all()
    return render(request,'development/model_backend.html',{'rows': rows})

@login_required
def backend_detail(request, backend_name):
    #rows = Backend.objects.select_related().all()
    #return render(request,'development/backend_detail.html',{'rows': rows})
    backendcheckmodel = get_object_or_404(BackendCheck,backend_name=backend_name)
    form = BackendCheckForm(request.POST or None, instance=backendcheckmodel)
    if form.is_valid():
        backendcheckmodel = form.save()
        return render(request,'development/model_backend_detail.html',{'form': form})
    return render(request,'development/model_backend_detail.html',{'form': form})

@login_required
def action_backend_detail(request, action, backend_name):
    if request.method == 'POST':
        if action == 'add':
            form = BackendCheckForm(request.POST or None)
            if form.is_valid():
                backendcheckmodel = form.save()
            return redirect("backend")
    else:
        if action == 'delete':
            backendcheckmodel = get_object_or_404(BackendCheck,backend_name=backend_name)
            backendcheckmodel.delete()
            return redirect("backend")
        form = BackendCheckForm()  
    return render(request,'development/model_backend_detail.html',{'form': form})

@login_required
def backend_server(request, backend_name):
    rows = BackendServer.objects.filter(backend__name=backend_name)
    return render(request,'development/model_backend_server.html',{'rows': rows, 'backend_name': backend_name})

@login_required
def backend_server_detail(request, backend_server_name):
    #rows = Backend.objects.select_related().all()
    #return render(request,'development/backend_detail.html',{'rows': rows})
    logging.debug(request.method)
    logging.debug(backend_server_name)
    backendserveroptionmodel = get_object_or_404(BackendServerOption,backend_server_name=backend_server_name)
    form = BackendServerOptionForm(request.POST or None, instance=backendserveroptionmodel)
    if form.is_valid():
        backendserveroptionmodel = form.save()
        return render(request,'development/model_backend_detail.html',{'form': form})
    return render(request,'development/model_backend_server_detail.html',{'form': form})

@login_required
def action_backend_server_detail(request, action, backend_name, backend_server_name):
    print request.method
    print action
    print backend_name
    print backend_server_name
    if request.method == 'POST':
        if action == 'add':
            print "add server"
            form = BackendServerOptionForm(request.POST or None)
            if form.is_valid():
                print "add server valid"
                backendserveroptionmodel = form.save()
            else:
                print "add server invalid"
            return redirect("backend_server", backend_name=backend_name)
    else:
        if action == 'delete':
            backendserveroptionmodel = get_object_or_404(BackendServerOption,backend_server_name=backend_server_name)
            backendserveroptionmodel.delete()
            return redirect("backend_server", backend_name=backend_name)
        backendmodel = get_object_or_404(Backend,name=backend_name)
        form = BackendServerOptionForm(initial={'backend': backendmodel})  
    return render(request,'development/model_backend_server_detail.html',{'form': form})



@login_required
def formset_server_detail(request, server_name):
    backenserver = BackendServer.objects.get(pk=server_name)
    form=BackendServerForm(request.POST or None)
    ServerDetailFormSet = inlineformset_factory(BackendServer, ServerOption , can_delete=False)
    if request.method == "POST":
        formset = ServerDetailFormSet(request.POST, request.FILES, instance=backenserver)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return render(request, "development/formset_server_detail.html", { "formset": formset, "form" : form})
    else:
        formset = ServerDetailFormSet(instance=backenserver)
    return render(request, "development/formset_server_detail.html", { "formset": formset, "form" : form})

@login_required
def server_detail(request, server_name):
    logger.debug(server_name)
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ServerDetailForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('../server_detail/')
            bs = BackendServer.objects.filter(name=form.cleaned_data['name'])
            servers = ServerOption.objects.filter(backend_server__name=form.cleaned_data['name'])
            for bb in bs:
                bb.address = form.cleaned_data['address']
                bb.port = form.cleaned_data['port']
                bb.maxconn = form.cleaned_data['maxconn']
                bb.save()
                for ss in bb.server_option.all():
                    ss.check = form.cleaned_data['check']
                    ss.check_inter = form.cleaned_data['check_inter']
                    ss.check_fall = form.cleaned_data['check_fall']
                    ss.cookie_value = form.cleaned_data['cookie_value']
                    logger.debug(ss.check_fall)
                    ss.save()
            #serverdetailmodel = form.save()
            return render(request,'development/server_detail.html',{'servers': servers, 'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #logger.debug(s.backend_server.name)
        form = ServerDetailForm()
        servers = ServerOption.objects.filter(backend_server__name=server_name)
        for ss in servers:
            logger.debug(dir(ss))
            form.fields['name'].widget.attrs["disabled"] = True
            form.fields["name"].initial = ss.backend_server.name
            form.fields["address"].initial = ss.backend_server.address
            form.fields["port"].initial = ss.backend_server.port
            form.fields["maxconn"].initial = ss.backend_server.maxconn
            form.fields["check"].initial = ss.check
            form.fields["check_inter"].initial = ss.check_inter
            form.fields["check_fall"].initial = ss.check_fall
            form.fields["cookie_value"].initial = ss.cookie_value
    return render(request,'development/server_detail.html',{'servers': servers, 'form': form})

@login_required
def action_server_detail(request, action, backend_name, server_name):
    logger.debug(action)
    logger.debug(server_name)
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ServerDetailForm(request.POST)
        db_backend = Backend.objects.filter(name=backend_name)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('../server_detail/')
            new_backend_server = BackendServer()
            new_backend_server.name = form.cleaned_data['name']
            new_backend_server.backend_id=backend_name
            new_backend_server.address = form.cleaned_data['address']
            new_backend_server.port = form.cleaned_data['port']
            new_backend_server.maxconn = form.cleaned_data['maxconn']
            new_backend_server.save() 
               
            new_server_option = ServerOption()
            new_server_option.backend_server_id = form.cleaned_data['name']
            new_server_option.check = form.cleaned_data['check']
            new_server_option.check_inter = form.cleaned_data['check_inter']
            new_server_option.check_fall = form.cleaned_data['check_fall']
            new_server_option.cookie_value = form.cleaned_data['cookie_value']
            
            new_backend_server.server_option.add(new_server_option)
            for local_db_backend in db_backend:
                local_db_backend.backend_server.add(new_backend_server)
            return redirect("../../../../backend_server/" + backend_name)

    # if a GET (or any other method) we'll create a blank form
    else:
        #logger.debug(s.backend_server.name)
        if action == 'delete':
            ServerOption.objects.filter(backend_server__name=server_name).delete()
            BackendServer.objects.filter(name=server_name).delete()
            return redirect("../../../../backend_server/" + backend_name)
            
        form = ServerDetailForm()

    return render(request,'development/action_server_detail.html',{'form': form, 'action': action})


def upload_file(request, frontend_name):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],form.cleaned_data['file_name'])
            bindoptionmodel = get_object_or_404(BindOption,frontend_name=frontend_name)
            bindoptionmodel.crt_name = form.cleaned_data['file_name']
            bindoptionmodel.save()
            return HttpResponseRedirect('/frontend_detail/'+ frontend_name +'/')
    else:
        form = UploadFileForm()
    return render_to_response('development/upload.html', {'form': form}, context_instance=RequestContext(request))

def handle_uploaded_file(f, file_name):
    with open('/tmp/' + file_name + ".pem", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    