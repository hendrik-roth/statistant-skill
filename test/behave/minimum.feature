Feature: calculate-minimum
  Scenario: calculate minimum
    Given an english speaking user
    When the user says "tell me the smallest value of x in test"
    Then "statistant-skill" should reply with exactly "The smallest value is 2.0"

  Scenario: calculate minimum alternative
    Given an english speaking user
    When the user says "what is the smallest value of x in test"
    Then "statistant-skill" should reply with exactly "The smallest value is 2.0"
