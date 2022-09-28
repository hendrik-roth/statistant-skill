Feature: calculate-quartile
  Scenario: calculate first quartile
    Given an english speaking user
    When the user says "what is the value of the first quartile of x in test"
    Then "statistant-skill" should reply with exactly "The first quartile is 14.25"

  Scenario: calculate second quartile
    Given an english speaking user
    When the user says "what is the value of the 2nd quartile of x in test"
    Then "statistant-skill" should reply with exactly "The quartile range is 28.5"

  Scenario: calculate third quartile
    Given an english speaking user
    When the user says "what is the value of the 3rd quartile of x in test"
    Then "statistant-skill" should reply with exactly "The quartile range is 45.75"
