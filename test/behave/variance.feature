Feature: calculate-variance
  Scenario: calculate variance
    Given an english speaking user
    When the user says "tell me the variance of x in test"
    Then "statistant-skill" should reply with "The variance is 412.667"