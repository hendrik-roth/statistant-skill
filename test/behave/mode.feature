Feature: calculate-mode
  Scenario: calculate mode x
    Given an english speaking user
    When the user says "tell me the mode of x in test"
    Then "statistant-skill" should reply with exactly "The mode is [50.0, 24.0, 52.0, 2.0, 33.0, 11.0]"

  Scenario: calculate mode z
    Given an english speaking user
    When the user says "tell me the mode of z in test"
    Then "statistant-skill" should reply with exactly "The mode is [2.0]"

  Scenario: calculate mode z alternative
    Given an english speaking user
    When the user says "what is the mode of z in test"
    Then "statistant-skill" should reply with exactly "The mode is [2.0]"
