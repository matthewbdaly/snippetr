from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.core.cache import cache

# Create your models here.
class Snippet(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pub_date:
            self.pub_date = timezone.now()
        if not self.slug:
            self.slug = slugify(unicode(self.title))
        super(Snippet, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.pub_date.year, self.pub_date.month, self.slug)

    def __unicode__(self):
        return self.title


# Define signals
def new_snippet(sender, instance, created, **kwargs):
    cache.clear()

# Set up signals
post_save.connect(new_snippet, sender=Snippet)
