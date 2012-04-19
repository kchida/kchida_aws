from django.conf import settings
from django.conf.urls import patterns, include, url

from apps.user.views import (login, register, user_account, logout)

urlpatterns = patterns('',
    
    # Site non-modal login.
    url(r'^login/$', login, name='login_view'),
    
    # Site user registration -- request username and password only. 
    # Case 1: Go here following new oauth user creation.
    # Case 2: Go here via direct register link.
    url(r'^register/$', register, name='register_view'),
    
    # Case 1: Redirect to here following social_auth associate. 
    # Case 2: Redirect to here following social_auth disassociate. 
    # Case 3: Go here via direct user account link.
    url(r'^user-account/$', user_account, name='user_account_view'),
    
    url(r'^logout/$', logout, name='logout_view'), 
    #url(r'', include('apps.user.urls')),
)
