@business-critical @api
Feature: Capacity and wait-list management
  So that an event is never overbooked
  As an event coordinator
  I want places and the wait-list to follow one clear state model

  Scenario: Registration at the last available place
    Given a published event with one place remaining
    When two eligible volunteers register
    Then exactly one new registration is confirmed
    And exactly one new registration is wait-listed
    And the number of confirmed volunteers does not exceed capacity

  Scenario: Cancellation releases a place fairly
    Given a full event with two wait-listed volunteers
    When a confirmed volunteer cancels
    Then the oldest wait-listed volunteer is promoted
    And the second wait-listed volunteer remains waiting
