Feature: calculate-quantile
  Scenario: calculate 0.1 quantile
    Given an english speaking user
    When the user says "tell me the 10 percentile quantile of x in test"
    Then "statistant-skill" should reply with exactly "The 0.1 quantile is 6.5"

  Scenario: calculate 0.1 quantile alternative
    Given an english speaking user
    When the user says "what is the 10 percentile quantile of x in test"
    Then "statistant-skill" should reply with exactly "The 0.1 quantile is 6.5"
