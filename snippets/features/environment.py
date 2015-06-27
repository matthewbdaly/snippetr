from splinter.browser import Browser
from snippets.tests import UserFactory

def before_all(context):
    context.browser = Browser('django')
    context.user = UserFactory()

def after_all(context):
    context.browser.quit()
    context.browser = None
