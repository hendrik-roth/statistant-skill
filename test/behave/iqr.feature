Feature: calculate-iqr
  Scenario: calculate iqr
    Given an english speaking user
    When the user says "tell me the quartile of x in test"
    Then "statistant-skill" should reply with "The quartile range is 31.5"

  Scenario: calculate iqr alternative
    Given an english speaking user
    When the user says "what is the quartile of x in test"
    Then "statistant-skill" should reply with "The quartile range is 31.5"