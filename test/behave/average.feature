Feature: calculate-average
  Scenario: calculate average
    Given an english speaking user
    When the user says "tell me the average of x in test"
    Then "statistant-skill" should reply with "The average is 28.667"

  Scenario: calculate average alternative
    Given an english speaking user
    When the user says "what is the average of x in test"
    Then "statistant-skill" should reply with "The average is 28.667"