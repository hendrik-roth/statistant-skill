Feature: calculate-maximum
  Scenario: calculate maximum
    Given an english speaking user
    When the user says "tell me the top value of x in test"
    Then "statistant-skill" should reply with "The top value is 2"