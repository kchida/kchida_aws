
import logging

from django import forms
from django.conf import settings
#from django.contribute_to_classb.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login as django_login, logout as django_logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.template.response import TemplateResponse
#from django.utils.http import urlsafe_base64_decode
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm

from apps.user.forms import LoginForm, RegisterForm, SocialRegisterForm
from apps.user.models import MyUser

#@sensitive_post_parameters()
#@csrf_protect
#@never_cache
def login(request, template_name='login_page.html', auth_form=LoginForm):
    
    # Sanity check: this person already logged in.
    if request.user.is_authenticated():
        return HttpResponseRedirect('/') 
        
    if request.method == 'POST':
        
        form = auth_form(data=request.POST)
        
        if form.is_valid():
            
            django_login(request)  #, authentication_form=auth_form)

    else:
        form = auth_form()
        
    c = RequestContext(request, {'login_form': form}) 
        
    return render_to_response(template_name, context_instance=c)


def register(request, template_name='register_page.html', redirect_to='',
             register_form=RegisterForm, social_register_form=SocialRegisterForm,
             extra_context=None):
    
    # Flag to determine whether we are registering from scratch
    # or following social authorization.
    is_social_register = False
   
    # is_registered flag is true if the user has setup their email and
    # password using the site registration form. 
    try: 
        if request.user.is_registered:
            return HttpResponseRedirect('/') 
    except:
        pass
    
    # If current user is already authenticated, they must have logged in
    # through social auth; they still need to register their email and pwd.    
    # social_register_form will not create a new user.
    if request.user.is_authenticated():
        _register_form = social_register_form
        initial=dict(username=request.user.username, email=request.user.email)
        is_social_register = True
    
    # register_form WILL create a new user via ModelForms
    else:
        _register_form = register_form
        initial = None
        
    if request.method == 'POST':
        form = _register_form(request.POST, initial=initial)
        if form.is_valid():
            if is_social_register:
                _user = User.objects.get(id=request.user.pk)
                _cleaned_data = form.cleaned_data
                _user.username = _cleaned_data['username']
                _user.email = _cleaned_data['email']
                _user.set_password(_cleaned_data['password1'])
                _user.is_registered = True
                _user.save()
            else:
                # For regular registration, form is a ModelForm so the save()
                # method is used to create new user in database.
                form.save()
                _user = User.objects.get(username=form.cleaned_data['username'])
                _user.is_registered = True
                _user.save()
            
            return HttpResponseRedirect('/')

    # Method is GET.
    else:
        form = _register_form(initial)
    
    # Following code handles GET methods and errors during POST.
    context = {
        'register_form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)
    
#TODO profiles: avatar, bookmarks, first/last name, etc
def user_account(request):            
    pass

def logout(request):
    """ 
    Wraps django logout view to perform any cleanup actions, if any, and 
    redirects to LOGIN_URL.
    """
    django_logout(request, next_page=settings.LOGIN_URL)

    return HttpResponseRedirect('/') 

#TODO Email registration/activation_complete

#TODO Permissions