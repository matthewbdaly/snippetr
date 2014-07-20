from django.conf.urls import patterns, url, include
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from snippets.models import Snippet
from snippets.forms import SnippetForm

urlpatterns = patterns('',
    # Social integration
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Auth
    url('', include('django.contrib.auth.urls', namespace='auth')),

    # Index - create new snippet
    url(r'^$', CreateView.as_view(
        model=Snippet,
        form_class=SnippetForm,
        )),

    # Individual posts
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(
        model=Snippet,
        )),
)
