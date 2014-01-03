from django.db import models
from django.utils import timezone

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
