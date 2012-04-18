from apps.redirects.models import Redirect
from django import http
from apps.urlrouter.base import URLHandler



# The following handlers are registered under settings.URL_ROUTE_HANDLERS

class RedirectRoutes(URLHandler):
    model = Redirect

    def show(self, request, redirect):
        if not redirect.redirect_to:
            return http.HttpResponseGone()
        return http.HttpResponsePermanentRedirect(redirect.redirect_to)
