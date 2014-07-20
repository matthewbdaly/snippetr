from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
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


class SnippetDetailView(GetRequestAndUserMixin, DetailView):
    """
    View for displaying a snippet
    """
    model = Snippet


class SnippetCreateView(GetRequestAndUserMixin, CreateView):
    """
    View for creating a snippet
    """
    model = Snippet
    form_class = SnippetForm


class LoginView(GetRequestAndUserMixin, TemplateView):
    """
    View for requiring login
    """
    template_name = 'registration/login.html'
