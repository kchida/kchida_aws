# Load the siteconf module
from django.conf import settings
from django.utils.importlib import import_module

# Originally created to load dbindex. Not sure if there is use for it anymore.
SITECONF_MODULE = getattr(settings, 'AUTOLOAD_SITECONF', settings.ROOT_URLCONF)
import_module(SITECONF_MODULE)
