from django.test import TestCase, LiveServerTestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from snippets.models import Snippet
from snippets.forms import SnippetForm
from snippets.views import LoginView, SnippetCreateView, SnippetDetailView
import factory.django
from unittest.mock import patch, MagicMock

# Factories for tests
class SnippetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Snippet
        django_get_or_create = (
            'title',
            'content',
            'slug',
            'pub_date'
        )

    title = 'My snippet'
    content = 'This is my snippet'
    slug = 'my-snippet'
    pub_date = timezone.now()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = 'bob@example.com'
    username = 'bobsmith'
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_superuser = True
    is_staff = True
    is_active = True


# Create your tests here.
class SnippetTest(TestCase):
    def test_create_snippet(self):
        # Create the snippet
        snippet = SnippetFactory()

        # Check we can find it
        all_snippets = Snippet.objects.all()
        self.assertEqual(len(all_snippets), 1)
        only_snippet = all_snippets[0]
        self.assertEqual(only_snippet, snippet)

        # Check attributes
        self.assertEqual(only_snippet.title, 'My snippet')
        self.assertEqual(only_snippet.content, 'This is my snippet')
        self.assertEqual(only_snippet.slug, 'my-snippet')
        self.assertEqual(only_snippet.pub_date.day, snippet.pub_date.day)
        self.assertEqual(only_snippet.pub_date.month, snippet.pub_date.month)
        self.assertEqual(only_snippet.pub_date.year, snippet.pub_date.year)
        self.assertEqual(only_snippet.pub_date.hour, snippet.pub_date.hour)
        self.assertEqual(only_snippet.pub_date.minute, snippet.pub_date.minute)
        self.assertEqual(only_snippet.pub_date.second, snippet.pub_date.second)


class SnippetFormTest(TestCase):
    """
    Test the snippet form
    """
    def setUp(self):
        self.user = UserFactory()

    def test_empty_form(self):
        """
        Test a form with no content
        """
        form = SnippetForm()
        self.assertFalse(form.is_valid())

    def test_completed_form(self):
        """
        Test a form with content
        """
        data = {
            'title': 'My snippet',
            'content': 'This is my snippet'
        }
        form = SnippetForm(data)
        self.assertTrue(form.is_valid())


class BaseViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.factory = RequestFactory()


class LoginViewTest(BaseViewTest):
    """
    Test the Login view
    """
    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('login'))
        request.user = self.user
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['user'], self.user)
        self.assertEqual(response.context_data['request'], request)


class SnippetCreateViewTest(BaseViewTest):
    """
    Test the snippet create view
    """
    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('snippet_create'))
        request.user = self.user
        response = SnippetCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['user'], self.user)
        self.assertEqual(response.context_data['request'], request)

    @patch('snippets.models.Snippet.save', MagicMock(name="save"))
    def test_post(self):
        """
        Test post requests
        """
        # Create the request
        data = {
            'title': 'My snippet',
            'content': 'This is my snippet'
        }
        request = self.factory.post(reverse('snippet_create'), data)
        request.user = self.user

        # Get the response
        response = SnippetCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)

        # Check save was called
        self.assertTrue(Snippet.save.called)
        self.assertEqual(Snippet.save.call_count, 1)


class SnippetDetailViewTest(BaseViewTest):
    """
    Test the snippet create view
    """
    def test_get(self):
        """
        Test GET requests
        """
        snippet = SnippetFactory()
        url = reverse('snippet_detail', args=[snippet.pub_date.year,snippet.pub_date.month,snippet.slug])
        request = self.factory.get(url)
        request.user = self.user
        response = SnippetDetailView.as_view()(request, slug=snippet.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['user'], self.user)
        self.assertEqual(response.context_data['request'], request)


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()


class AdminTest(BaseAcceptanceTest):

    def test_login(self):
        # Create user
        user = UserFactory()

        # Get login page
        response = self.client.get('/admin/', follow=True)

        # Check response code
        self.assertEqual(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content.decode('utf-8'))

        # Log the user in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content.decode('utf-8'))

    def test_logout(self):
        # Create user
        user = UserFactory()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content.decode('utf-8'))

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/admin/', follow=True)
        self.assertEqual(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content.decode('utf-8'))

    def test_create_snippet(self):
        # Create user
        user = UserFactory()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/snippets/snippet/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new snippet
        response = self.client.post('/admin/snippets/snippet/add/', {
                'title': 'My first snippet',
                'content': 'This is my first snippet',
                'pub_date_0': '2013-12-28',
                'pub_date_1': '22:00:04',
                'slug': 'my-first-snippet'
                },
                follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check new snippet now in database
        all_snippets = Snippet.objects.all()
        self.assertEqual(len(all_snippets), 1)

    def test_edit_snippet(self):
        # Create user
        user = UserFactory()

        # Create the snippet
        snippet = SnippetFactory()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Edit the post
        response = self.client.post('/admin/snippets/snippet/' + str(snippet.pk) + '/', {
            'title': 'My second snippet',
            'content': 'This is my second snippet',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04',
            'slug': 'my-second-snippet'
        },
        follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check post amended
        all_snippets = Snippet.objects.all()
        self.assertEqual(len(all_snippets), 1)
        only_snippet = all_snippets[0]
        self.assertEqual(only_snippet.title, 'My second snippet')
        self.assertEqual(only_snippet.content, 'This is my second snippet')
        self.assertEqual(only_snippet.slug, 'my-second-snippet')

    def test_delete_snippet(self):
        # Create user
        user = UserFactory()

        # Create the snippet
        snippet = SnippetFactory()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Delete the snippet
        response = self.client.post('/admin/snippets/snippet/' + str(snippet.pk) + '/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check post amended
        all_snippets = Snippet.objects.all()
        self.assertEqual(len(all_snippets), 0)


class SnippetViewTest(BaseAcceptanceTest):
    def test_view_snippet(self):
        # Create user
        user = UserFactory()

        # Create the snippet
        snippet = SnippetFactory()

        # Check new snippet now in database
        all_snippets = Snippet.objects.all()
        self.assertEqual(len(all_snippets), 1)
        only_snippet = all_snippets[0]
        self.assertEqual(only_snippet, snippet)

        # Fetch the snippet
        snippet_url = only_snippet.get_absolute_url()
        response = self.client.get(snippet_url)
        self.assertEqual(response.status_code, 200)

        # Check the snippet details are in the response
        self.assertTrue(snippet.title in response.content.decode('utf-8'))
        self.assertTrue(snippet.content in response.content.decode('utf-8'))
        self.assertTrue(str(snippet.pub_date.year) in response.content.decode('utf-8'))
        self.assertTrue(snippet.pub_date.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(snippet.pub_date.day) in response.content.decode('utf-8'))

    def test_create_snippet(self):
        # Create user
        user = UserFactory()

        # Try to get home page - should fail
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Create the snippet
        response = self.client.post('/', {
                'title': 'My first snippet',
                'content': 'This is my first snippet',
                },
                follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check the snippet is in the database
        all_snippets = Snippet.objects.all()
        self.assertEqual(len(all_snippets), 1)
        only_snippet = all_snippets[0]

        # Check the snippet attributes
        self.assertEqual(only_snippet.title, 'My first snippet')
        self.assertEqual(only_snippet.content, 'This is my first snippet')
        self.assertEqual(only_snippet.slug, 'my-first-snippet')

    def test_sitemap(self):
        # Create a snippet
        snippet = SnippetFactory()

        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
