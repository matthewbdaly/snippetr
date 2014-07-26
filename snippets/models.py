from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.core.cache import cache

# Create your models here.
class Snippet(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now())
    slug = models.SlugField(max_length=40, unique=True)

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.pub_date.year, self.pub_date.month, self.slug)

    def __unicode__(self):
        return self.title


# Define signals
def new_snippet(sender, instance, created, **kwargs):
    cache.clear()

# Set up signals
post_save.connect(new_snippet, sender=Snippet)
