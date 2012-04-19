from apps.blog.models import Blog, Post
from apps.blog.views import browse, show_post, latest_entries_feed
from apps.urlrouter.base import URLHandler

# The following handlers are registered under settings.URL_ROUTE_HANDLERS

class BlogRoutes(URLHandler):
    # This attribute will help signals to be identified.
    model = Blog

    def show(self, request, blog):
        if request.path == blog.get_internal_feed_url():
            return latest_entries_feed(request, blog)
        return browse(request, blog=blog)

    def get_urls(self, blog):
        yield blog.get_absolute_url()
        yield blog.get_internal_feed_url()

class BlogPostRoutes(URLHandler):
    model = Post
    show = staticmethod(show_post)

    def get_urls(self, post):
        if post.published:
            yield post.get_absolute_url()
