#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "haproxyweb.settings")

    from django.core.management import execute_from_command_line
#    from django.db import connection
#    cursor = connection.cursor()
#    if 'haproxy' in connection.introspection.table_names():
#        print 'exists'
#    else:
#        print 'no exists'
        
    execute_from_command_line(sys.argv)
