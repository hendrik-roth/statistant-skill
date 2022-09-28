Feature: calculate-quartile
  Scenario: calculate first quartile
    Given an english speaking user
    When the user says "what is the value of the first quartile of x in test"
    Then "statistant-skill" should reply with exactly "The first quartile is 14.25"

  Scenario: calculate second quartile
    Given an english speaking user
    When the user says "what is the value of the second quartile of x in test"
    Then "statistant-skill" should reply with exactly "The second quartile is 28.5"

  Scenario: calculate third quartile
    Given an english speaking user
    When the user says "what is the value of the third quartile of x in test"
    Then "statistant-skill" should reply with exactly "The third quartile is 45.75"
