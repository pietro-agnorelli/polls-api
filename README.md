This client is used to manage a simple polling sistem, in which authenticated users can create polls and vote, while results and a list of all polls is visible to every user.
the authenticaton is implemented using django REST framework token authentication
the following is a list of endpoints with request methods and functionalities:
-/api/v1/auth/register/    "POST"    allows registration of new users, returns auth token
-/api/v1/auth/login/    "POST"    allows user login, returns auth token
-/api/v1/polls/    "GET"    returns all polls
-/api/v1/polls/    "POST"    create new poll
-/api/v1/polls/:id/    "GET"    returns selected poll
-/api/v1/polls/:id/    "DELETE"    deletes selected view
-/api/v1/polls/:id/vote/    "POST"    creates new vote for selected view, if user has already voted, deletes old one before saving
-/api/v1/polls/:id/vote/    "GET"    returns results for selected poll

This api is used in this client: https://pietro-agnorelli.github.io/polls-api-client/
