from django.contrib import admin

# Register your models here.
from haproxygui.models import *

admin.site.register(Default)
admin.site.register(Frontend)
admin.site.register(FrontendBind)
admin.site.register(BindOption)
admin.site.register(Backend)
admin.site.register(BackendCheck)
admin.site.register(BackendServer)
admin.site.register(ServerOption)
admin.site.register(BackendServerOption)
admin.site.register(SSLFile)


