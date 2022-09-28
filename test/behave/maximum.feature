Feature: calculate-maximum
  Scenario: calculate maximum
    Given an english speaking user
    When the user says "tell me the top value of x in test"
    Then "statistant-skill" should reply with exactly "The top value is 2"

  Scenario: calculate maximum alternative
    Given an english speaking user
    When the user says "what is the top value of x in test"
    Then "statistant-skill" should reply with exactly "The top value is 2"
