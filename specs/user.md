Scenario: Create a normal user
  Given nothing
  When user sends username, password and email
  Then a normal user account is created

Scenario: Create a company user
  Given nothing
  When user sends username, password, email and is_company=True
  Then a "company" account is created

Scenario: Authentication: get my profile
  Given authenticated user Bob
  When Bob asks his profile
  Then he receives his profile (username, email, is_company)

Scenario: Authentication: unauthenticated get my profile -> error
  Given unauthenticated user
  When user asks his profile
  Then he receives 403 error

