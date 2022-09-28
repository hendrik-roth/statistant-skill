Feature: calculate-sum
  Scenario: calculate sum
    Given an english speaking user
    When the user says "tell me the sum of x in test"
    Then "statistant-skill" should reply with exactly "The sum is 172"

  Scenario: calculate sum
    Given an english speaking user
    When the user says "what is the sum of x in test"
    Then "statistant-skill" should reply with exactly "The sum is 172"
