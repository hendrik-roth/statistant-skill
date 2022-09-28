Feature: calculate-variance
  Scenario: calculate variance
    Given an english speaking user
    When the user says "tell me the variance of x in test"
    Then "statistant-skill" should reply with exactly "The variance is 412.667"

  Scenario: calculate variance alternative
    Given an english speaking user
    When the user says "what is the variance of x in test"
    Then "statistant-skill" should reply with exactly "The variance is 412.667"
