#! /usr/bin/env python
import sys
import os
import django.core.handlers.wsgi

sys.path.append('/opt/django-projects/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'foo.settings'
application = django.core.handlers.wsgi.WSGIHandler()
