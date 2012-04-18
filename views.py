
import logging

from django import forms
from django.conf import settings
#from django.contribute_to_classb.auth import REDIRECT_FIELD_NAME
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
#from django.contrib.auth.tokens import default_token_generator
#from django.contrib.auth.views import login as login_django
#from django.core.exceptions import ObjectDoesNotExist, ValidationError
#from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
#from django.utils.http import urlsafe_base64_decode
#from django.views.decorators.csrf import csrf_protect
#from django.views.decorators.cache import never_cache

from apps.user.forms import LoginForm, RegisterForm



# Replaced by CMS page. Context is provided by user.context_processor.login_reg
def home(request, template_name='home.html',
         login_form=LoginForm, register_form=RegisterForm):
    """
    View to handle request to go to home url.
    """
    c = RequestContext(request, {'login_url': settings.LOGIN_URL,
                                 'login_form': login_form,
                                 'register_form': register_form,})
    
    return render_to_response(template_name, context_instance=c)
