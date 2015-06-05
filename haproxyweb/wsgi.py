"""
WSGI config for haproxyweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import sys
#sys.path.append('/usr/share/haproxyweb')

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),"..")))
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "haproxyweb.settings")
#os.environ['DJANGO_SETTINGS_MODULE'] = 'haproxyweb.production_settings'
os.environ['DJANGO_SETTINGS_MODULE'] = 'haproxyweb.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
