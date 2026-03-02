Scenario: Create a theater
  Given a company user
  When user sends a theater name and address
  Then a theater is created

Scenario: Non-company user cannot create a theater
  Given a normal user (is_company=False)
  When user tries to create a theater
  Then he receives a 403 error

Scenario: Add a screening to a theater
  Given a company user who owns a theater
  When user sends movie name, date and theater id
  Then a screening is created for that theater

Scenario: Cancel a screening
  Given a company user who owns a theater with an existing screening
  When user cancels the screening
  Then the screening is removed

Scenario: Only the theater owner can cancel a screening
  Given a company user who does NOT own the theater
  When user tries to cancel a screening of that theater
  Then he receives a 403 error
