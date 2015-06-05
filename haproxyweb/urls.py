from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from haproxygui import views_class
from django.contrib.auth.decorators import login_required
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'haproxyweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'haproxygui.views.status', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^default/', 'haproxygui.views.default', name='default'),
    url(r'^dummy/', 'haproxygui.views.dummy', name='dummy'),
###frontend
#    url(r'^frontend/', 'haproxygui.views.frontend', name='frontend'),
    url(r'^frontend/list/$', login_required(views_class.FrontendList.as_view()), name='frontend_list'),
    url(r'^frontend/add/$', login_required(views_class.FrontendCreate.as_view()), name='frontend_add'),
    url(r'^frontend/delete/(?P<pk>.*)/$', login_required(views_class.FrontendDelete.as_view()), name='frontend_delete'),
    url(r'^frontend/(?P<pk>.*)/$', login_required(views_class.FrontendUpdate.as_view()), name='frontend_update'),
#    url(r'^frontend_detail/(?P<frontend_name>.*)/$', 'haproxygui.views.frontend_detail'),
#    url(r'^(?P<action>.*)/frontend_detail/(?P<frontend_name>.*)/', 'haproxygui.views.action_frontend_detail'),
###frontend_bind
    url(r'^frontend_bind/list/(?P<frontend_name>.*)/$', login_required(views_class.FrontendBindList.as_view()), name='frontend_bind_list'),
    url(r'^frontend_bind/add/(?P<frontend_name>.*)/$', login_required(views_class.FrontendBindCreate.as_view()), name='frontend_bind_add'),    
    url(r'^frontend_bind/delete/(?P<pk>.*)/$', login_required(views_class.FrontendBindDelete.as_view()), name='frontend_bind_delete'),    
    url(r'^frontend_bind/(?P<pk>.*)/$', login_required(views_class.FrontendBindUpdate.as_view()), name='frontend_bind_update'),
###backend
    url(r'^backend/list/$', login_required(views_class.BackendList.as_view()), name='backend_list'),
    url(r'^backend/add/$', login_required(views_class.BackendCreate.as_view()), name='backend_add'),
    url(r'^backend/delete/(?P<pk>.*)/$', login_required(views_class.BackendDelete.as_view()), name='backend_delete'),
    url(r'^backend/(?P<pk>.*)/$', login_required(views_class.BackendUpdate.as_view()), name='backend_update'),
#    url(r'^backend/', 'haproxygui.views.backend', name='backend'),
#    url(r'^backend_detail/(?P<action>.*)/(?P<backend_name>.*)/', 'haproxygui.views.action_backend_detail'),
#    url(r'^backend_detail/(?P<backend_name>.*)/', 'haproxygui.views.backend_detail'),
###backend_server
    url(r'^backend_server/list/(?P<backend_name>.*)/$', login_required(views_class.BackendServerList.as_view()), name='backend_server_list'),
    url(r'^backend_server/add/(?P<backend_name>.*)/$', login_required(views_class.BackendServerCreate.as_view()), name='backend_server_add'),
    url(r'^backend_server/delete/(?P<pk>.*)/$', login_required(views_class.BackendServerDelete.as_view()), name='backend_server_delete'),
    url(r'^backend_server/(?P<pk>.*)/$', login_required(views_class.BackendServerUpdate.as_view()), name='backend_server_update'),

#    url(r'^backend_server/(?P<backend_name>.*)/', 'haproxygui.views.backend_server', name='backend_server'),
#    url(r'^backend_server_detail/(?P<action>.*)/(?P<backend_name>.*)/(?P<backend_server_name>.*)/', 'haproxygui.views.action_backend_server_detail'),
#    url(r'^backend_server_detail/(?P<backend_server_name>.*)/', 'haproxygui.views.backend_server_detail'),

#    url(r'^server_detail/(?P<server_name>.*)/', 'haproxygui.views.server_detail'),
#    url(r'^(?P<action>.*)/(?P<backend_name>.*)/server_detail/(?P<server_name>.*)/', 'haproxygui.views.action_server_detail'),
#    url(r'^server_detail/(?P<server_name>.*)/', 'haproxygui.views.formset_server_detail'),

    url(r'^accounts/login/$', 'haproxygui.views.login', name='login'),
    url(r'^accounts/logout/$', 'haproxygui.views.logout', name='logout'),
    url(r'^status/$', 'haproxygui.views.status', name='status'),

    url(r'^ssl/add/$', login_required(views_class.SSLFileCreate.as_view()), name='sslfile_add'),
    url(r'^ssl/list/$', login_required(views_class.SSLFileList.as_view()), name='sslfile_list'),
    url(r'^ssl/delete/(?P<pk>.*)/$', login_required(views_class.SSLFileDelete.as_view()), name='sslfile_delete'),    

    url(r'^upload/(?P<frontend_name>.*)/', 'haproxygui.views.upload_file'),
    url(r'^hello/', 'haproxygui.views_sqlalchemy.hello_world'),
    url(r'^database/', 'haproxygui.views_sqlalchemy.database'),
    url(r'^theme/', 'haproxygui.views.theme'),
)

urlpatterns += patterns(
    'django.contrib.staticfiles.views',
    url(r'^(?:index.html)?$', 'serve', kwargs={'path': 'index.html'}),
    url(r'^(?P<path>(?:js|css|image|dist|bower_components|less|pages)/.*)$', 'serve'),
)