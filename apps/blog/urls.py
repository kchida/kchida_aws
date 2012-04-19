from django.conf.urls.defaults import *

urlpatterns = patterns('apps.blog.views',
    (r'^review/(?P<review_key>.*)$', 'review'),
)
