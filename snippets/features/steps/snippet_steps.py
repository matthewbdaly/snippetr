from urlparse import urljoin

from behave import *

@given(u'I am not logged in')
def impl(context):
    context.browser.cookies.delete()

@given(u'I am logged in')
def impl(context):
    context.browser.cookies.delete()
    full_url = urljoin(context.config.server_url, '/admin/')
    context.browser.visit(full_url)
    context.browser.fill('username', 'bobsmith')
    context.browser.fill('password', 'password')
    button = context.browser.find_by_css('input[type="submit"]')
    button.click()
    assert context.browser.is_text_present('Welcome') == True

@then(u'I should see the text "{text}"')
def impl(context, text):
    assert context.browser.is_text_present(text) == True

@when(u'I visit the "{path}" page')
def impl(context, path):
    full_url = urljoin(context.config.server_url, path)
    context.browser.visit(full_url)

@when(u'I fill in the "{field}" field with "{text}"')
def impl(context, field, text):
    context.browser.fill(field, text)

@when(u'I submit the form')
def impl(context):
    button = context.browser.find_by_css('input[type="submit"]')
    button.click()
