Feature: calculate-range
  Scenario: calculate range
    Given an english speaking user
    When the user says "tell me the range of x in test"
    Then "statistant-skill" should reply with exactly "The range is 50"

  Scenario: calculate range
    Given an english speaking user
    When the user says "what is the range of x in test"
    Then "statistant-skill" should reply with exactly "The range is 50"
