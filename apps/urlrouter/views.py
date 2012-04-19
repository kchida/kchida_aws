from apps.urlrouter.api import handlers
from apps.urlrouter.models import URLRoute
from django.shortcuts import get_object_or_404

# Called by urlrouter middleware once url has been determined not
# to match any regex's in any url.py files.
def show(request, url):
    route = get_object_or_404(URLRoute, url=url)
    return handlers[route.handler].dispatch(request, route.target)
