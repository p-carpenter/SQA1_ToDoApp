Feature: Task Tags
  As a user
  I want to add tags to my tasks
  So I can organize them better

  Scenario: Create a task with tags
    Given I am logged in
    And I am on the task creation page
    When I create a task with title "My Task" and tags "urgent, home"
    Then the task should be created successfully
    And the task should have tags "urgent, home"