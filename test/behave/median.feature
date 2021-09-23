Feature: calculate-median
  Scenario: calculate median
    Given an english speaking user
    When the user says "tell me the median of x in test"
    Then "statistant-skill" should reply with "The average is 28.5"