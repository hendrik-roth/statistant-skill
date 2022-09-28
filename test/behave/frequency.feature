Feature: calculate-frequency
  Scenario: calculate absolute frequency
    Given an english speaking user
    When the user says "which absolute frequency has the value 2 of x in test"
    Then "statistant-skill" should reply with exactly "The absolute frequency is 1"

  Scenario: calculate relative frequency
    Given an english speaking user
    When the user says "which relative frequency has the value 2 of x in test"
    Then "statistant-skill" should reply with exactly "The relative frequency is 0.167"
