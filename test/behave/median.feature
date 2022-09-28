Feature: calculate-median
  Scenario: calculate median
    Given an english speaking user
    When the user says "tell me the median of x in test"
    Then "statistant-skill" should reply with exactly "The median is 28.5"

  Scenario: calculate median alternative
    Given an english speaking user
    When the user says "what is the median of x in test"
    Then "statistant-skill" should reply with exactly "The median is 28.5"
