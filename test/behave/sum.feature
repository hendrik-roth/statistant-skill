Feature: calculate-sum
  Scenario: calculate sum
    Given an english speaking user
    When the user says "tell me the sum of x in test"
    Then "statistant-skill" should reply with "The sum is 172"