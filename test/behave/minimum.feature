Feature: calculate-minimum
  Scenario: calculate minimum
    Given an english speaking user
    When the user says "tell me the smallest value of x in test"
    Then "statistant-skill" should reply with "The smallest value is 2"