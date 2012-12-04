import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'E:/DjangoProject/SignPass/settings.py'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = 'E:/DjangoProject/SignPass'
if path not in sys.path:
    sys.path.append(path)