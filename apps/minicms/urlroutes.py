from apps.minicms.models import Page
from django import http
from django.shortcuts import render
from apps.urlrouter.base import URLHandler



# The following handlers are registered under settings.URL_ROUTE_HANDLERS

class PageRoutes(URLHandler):
    model = Page

    def show(self, request, page):
        # TODO: Use permission check instead of is_superuser. But first
        # think the whole permission management through...
        if not page.published and not request.user.is_superuser:
            raise http.Http404('Not found')
        return render(request, 'minicms/page_detail.html', {'page': page})
