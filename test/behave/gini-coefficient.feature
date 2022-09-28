Feature: calculate-gini
  Scenario: calculate gini coefficient
    Given an english speaking user
    When the user says "tell me the gini coefficient of hello in test"
    Then "statistant-skill" should reply with exactly "The gini coefficient is 0.423"
