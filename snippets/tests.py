from django.test import TestCase, LiveServerTestCase, Client
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


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

    def test_login(self):
        # Get login page
        response = self.client.get('/admin/')

        # Check response code
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)

        # Log the user in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)

    def test_create_snippet(self):
        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/snippets/snippet/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new snippet
        response = self.client.post('/admin/snippets/snippet/add/', {
                'title': 'My first snippet',
                'content': 'This is my first snippet',
                'pub_date_0': '2013-12-28',
                'pub_date_1': '22:00:04',
                },
                follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content)

        # Check new snippet now in database
        all_snippets = Snippet.objects.all()
        self.assertEquals(len(all_snippets), 1)

    def test_edit_snippet(self):
        # Create the snippet
        snippet = Snippet()
        snippet.title = 'My snippet'
        snippet.content = 'This is my snippet'
        snippet.pub_date = timezone.now()
        snippet.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Edit the post
        response = self.client.post('/admin/snippets/snippet/1/', {
            'title': 'My second snippet',
            'content': 'This is my second snippet',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04'
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)

        # Check post amended
        all_snippets = Snippet.objects.all()
        self.assertEquals(len(all_snippets), 1)
        only_snippet = all_snippets[0]
        self.assertEquals(only_snippet.title, 'My second snippet')
        self.assertEquals(only_snippet.content, 'This is my second snippet')

    def test_delete_snippet(self):
        # Create the snippet
        snippet = Snippet()
        snippet.title = 'My snippet'
        snippet.content = 'This is my snippet'
        snippet.pub_date = timezone.now()
        snippet.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Delete the snippet
        response = self.client.post('/admin/snippets/snippet/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check post amended
        all_snippets = Snippet.objects.all()
        self.assertEquals(len(all_snippets), 0)
