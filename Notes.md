## Stateful versus stateless applications
This is one of the most important concepts in backend development and distributed systems.
Let's begin with a simple example.
Imagine logging into your Student Management application.
You enter your username and password. The backend verifies them. When you later request your profile, the backend needs to determine whether you're authenticated.
Where does the information that you logged in live?
The answer depends on how the application is designed.
### What is state?
State is information about a system's current condition that may affect what happens next.
Examples include:
- Whether a user is logged in.
- Which items are in a shopping cart.
- Whether a payment is pending or completed.
- Which messages a user has read.
- Which page of results a client is viewing.
State can exist in many places: a database, a browser, a server's memory, a cache, or a token carried by the client.
### Stateful application
A stateful application retains relevant client or session information on the server between requests.
Imagine a simplified server that stores login sessions in memory

```
sessions = {}

def login(username, session_id):
    sessions[session_id] = {
        "username": username,
        "logged_in": True
    }

def get_profile(session_id):
    return sessions.get(session_id)
```

### Stateless application
A stateless request-handling design does not depend on a particular application server retaining conversational session state between requests. Each request carries, or references, the information needed to process it.
For example, a client might send a signed access token in each request:
```GET /profile
Authorization: Bearer eyJ...```

The server validates the token and identifies the user.

A simplified flow:
1. The user logs in.
2. The backend issues an access token.
3. The client stores the token appropriately.
4. The client sends the token with each protected request.
5. The server validates it before returning protected data.
This resembles your earlier FastAPI JWT exercise.
Why statelessness can help scaling
Suppose there are three application servers:

<img width="1049" height="401" alt="image" src="https://github.com/user-attachments/assets/ed46d950-5e42-45ef-8a24-a7360addc6cc" />
