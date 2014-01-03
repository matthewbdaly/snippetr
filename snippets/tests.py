from django.test import TestCase
from django.utils import timezone
from snippets.models import Snippet

# Create your tests here.
class SnippetTest(TestCase):
    def test_create_snippet(self):
        # Create the snippet
        snippet = Snippet()

        # Set the attributes
        snippet.title = 'My snippet'
        snippet.content = 'This is my snippet'
        snippet.pub_date = timezone.now()

        # Save it
        snippet.save()

        # Check we can find it
        all_snippets = Snippet.objects.all()
        self.assertEquals(len(all_snippets), 1)
        only_snippet = all_snippets[0]
        self.assertEquals(only_snippet, snippet)

        # Check attributes
        self.assertEquals(only_snippet.title, 'My snippet')
        self.assertEquals(only_snippet.content, 'This is my snippet')
        self.assertEquals(only_snippet.pub_date.day, snippet.pub_date.day)
        self.assertEquals(only_snippet.pub_date.month, snippet.pub_date.month)
        self.assertEquals(only_snippet.pub_date.year, snippet.pub_date.year)
        self.assertEquals(only_snippet.pub_date.hour, snippet.pub_date.hour)
        self.assertEquals(only_snippet.pub_date.minute, snippet.pub_date.minute)
        self.assertEquals(only_snippet.pub_date.second, snippet.pub_date.second)
