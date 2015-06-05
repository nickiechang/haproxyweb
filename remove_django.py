import sys,os

sys.path = sys.path[1:]

try:
    import django
    [os.system('rm -fR ' +  p) for p in django.__path__]
except:
    print 'except'