from django.db import models
from django.utils import timezone

# Create your models here.
class Snippet(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now())
