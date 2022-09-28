Feature: calculate-herfindahl
  Scenario: calculate herfindahl index
    Given an english speaking user
    When the user says "tell me the herfindahl index of hello in test"
    Then "statistant-skill" should reply with exactly "The herfindahl index 0.163"
