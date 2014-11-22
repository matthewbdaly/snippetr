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
