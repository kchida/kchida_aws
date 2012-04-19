from apps.urlrouter import api
from apps.urlrouter.views import show
from django.conf import settings
from django.http import Http404

class URLRouterFallbackMiddleware(object):
    """ 
    Process 404 response after it has been determined that the requested url
    does not match regex's in any url.py files. urlroutes.py modules in app
    directories will be used to resolve instead.
    
    """
    
    def process_response(self, request, response):
        # Pass through if url matches entry in a url.py file.
        if response.status_code != 404:
            return response
        try:
            # TODO/XXX: Workaround for bug in Django. TemplateResponse.render()
            # isn't called after process_response(). Perhaps we need to use
            # process_template_response() instead?????
            new_response = show(request, request.path_info)
            if hasattr(new_response, 'render') and callable(new_response.render):
                new_response = new_response.render()
            return new_response
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
