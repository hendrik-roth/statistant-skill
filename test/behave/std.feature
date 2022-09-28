Feature: calculate-std
  Scenario: calculate std
    Given an english speaking user
    When the user says "tell me the standard deviation of x in test"
    Then "statistant-skill" should reply with exactly "The standard deviation is 20.314"

  Scenario: calculate std alternative
    Given an english speaking user
    When the user says "what is the standard deviation of x in test"
    Then "statistant-skill" should reply with exactly "The standard deviation is 20.314"
