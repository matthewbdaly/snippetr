Feature: Snippets

    In order to use the site
    As a user
    I want to be able to create and comment on snippets

    Scenario: Home page when not logged in
        Given I am not logged in
        When I visit the "/" page
        Then I should see the text "You need to log in to create a snippet"

    Scenario: Home page when not logged in
        Given I am logged in
        When I visit the "/" page
        Then I should see the text "Hello"

    Scenario: Create a snippet
        Given I am logged in
        When I visit the "/" page
        And I fill in the "title" field with "My snippet"
        And I fill in the "content" field with "This is my snippet"
        And I submit the form
        Then I should see the text "This is my snippet"
