Feature: calculate-iqr
  Scenario: calculate iqr
    Given an english speaking user
    When the user says "tell me the quartile range of x in test"
    Then "statistant-skill" should reply with exactly "The quartile range is 31.5"

  Scenario: calculate iqr alternative
    Given an english speaking user
    When the user says "what is the quartile range of x in test"
    Then "statistant-skill" should reply with exactly "The quartile range is 31.5"
