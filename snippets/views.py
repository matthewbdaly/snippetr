from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from snippets.forms import SnippetForm
from snippets.models import Snippet

class GetRequestAndUserMixin(object):
    """
    Mixin for getting the user and request and returning them as context data
    """
    def get_context_data(self, **kwargs):
        context = super(GetRequestAndUserMixin, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['request'] = self.request
        return context


class SnippetDetailView(DetailView, GetRequestAndUserMixin):
    """
    View for displaying a snippet
    """
    model = Snippet


class SnippetCreateView(CreateView, GetRequestAndUserMixin):
    """
    View for creating a snippet
    """
    model = Snippet
    form_class = SnippetForm
