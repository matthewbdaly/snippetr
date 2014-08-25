from django.conf.urls import patterns, url, include
from snippets.views import SnippetCreateView, SnippetDetailView, LoginView, anonymous_required
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from snippets.sitemap import SnippetSiteMap

# Define sitemaps
sitemaps = {
    'snippets': SnippetSiteMap
}

urlpatterns = patterns('',
    # Social integration
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Auth
    url('', include('django.contrib.auth.urls', namespace='auth')),

    # Comments
    (r'^comments/', include('django_comments.urls')),

    # Index - create new snippet
    url(r'^$', login_required(SnippetCreateView.as_view(
        ))),

    # Individual posts
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', SnippetDetailView.as_view(
        )),

    # Login
    url(r'^accounts/login/?$', anonymous_required(LoginView.as_view(
        ))),

    # Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap'),
)
