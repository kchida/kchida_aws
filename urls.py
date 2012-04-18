from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # Replaced by CMS page. Context is provided by user.context_processor.login_reg
    #url(r'^$', 'kchida_aws.views.home', name='home_view'),
    
    url(r'^blog/', include('apps.blog.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # All django-social-auth functions including social-auth login. 
    url(r'social', include('social_auth.urls')),
    
    # User-related functions including non-social-auth login.
    url(r'', include('apps.user.urls')),
)

# For development, django will serve static files (i.e. r'^static/.*' urls)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
