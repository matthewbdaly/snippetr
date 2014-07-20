from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from snippets.forms import SnippetForm
from snippets.models import Snippet
from django.conf import settings

def anonymous_required(func):
    """
    Require someone visiting this page to not be logged in
    """
    def as_view(request, *args, **kwargs): # pragma: no cover
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view


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
