Scenario: List movies currently showing
  Given nothing
  When user requests the list of movies
  Then he receives all movies that have at least one upcoming screening

Scenario: List screenings for a movie
  Given a movie title
  When user requests screenings for that movie
  Then he receives the list of theaters showing it with dates and times

Scenario: Book a seat
  Given authenticated user Bob, a movie name, a theater id and a scheduled date
  When Bob books a seat for that screening
  Then we call the theater's booking API (now:using dispacher)

Scenario: Unauthenticated user cannot book
  Given an unauthenticated user
  When user tries to book a seat
  Then he receives a 403 error

Scenario: Book a seat at an MK2 theater
  Given authenticated user Bob and an MK2 theater
  When Bob books a seat
  Then we call the MK2 booking API

Scenario: Book a seat at a UGC theater
  Given authenticated user Bob and a UGC theater
  When Bob books a seat
  Then we call the UGC booking API (different signature than MK2)

