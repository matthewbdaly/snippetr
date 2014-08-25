from snippets.models import Snippet
from django.contrib.sitemaps import Sitemap

class SnippetSiteMap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Snippet.objects.all()

    def lastmod(self, obj):
        return obj.pub_date
