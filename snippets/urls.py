from django.conf.urls import patterns, url, include
from snippets.views import SnippetCreateView, SnippetDetailView, LoginView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Social integration
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Auth
    url('', include('django.contrib.auth.urls', namespace='auth')),

    # Index - create new snippet
    url(r'^$', login_required(SnippetCreateView.as_view(
        ))),

    # Individual posts
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', SnippetDetailView.as_view(
        )),

    # Login
    url(r'^accounts/login/?$', LoginView.as_view(
        )),
)
