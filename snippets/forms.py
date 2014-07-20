from django.forms import ModelForm
from snippets.models import Snippet
from django.utils import timezone
from django.utils.text import slugify

class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        exclude = ['slug', 'pub_date', ]

    def save(self, commit=True):
        instance = super(SnippetForm, self).save(commit=False)
        instance.pub_date = timezone.now()
        instance.slug = slugify(instance.title)
        if commit: # pragma: no cover
            instance.save()
        return instance
