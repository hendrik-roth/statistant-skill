Feature: calculate-percentage-change
  Scenario: calculate percentage change
    Given an english speaking user
    When the user says "what is the percentage change from 2 to 4"
    Then "statistant-skill" should reply with "The percentage change from 2 to 4 is 100 percent"