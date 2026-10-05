client server architecture

Client
  |
  | HTTP Request
  ↓
Server
  |
  | HTTP Response
  ↓
Client

# Explain HTTP Request

An HTTP request contains:

Request
│
├── Method
├── URL
├── Headers
└── Body

# 2. HTTP Methods
| Method | Meaning       | CRUD   |
| ------ | ------------- | ------ |
| GET    | Retrieve data | Read   |
| POST   | Create data   | Create |
| PUT    | Update data   | Update |
| DELETE | Remove data   | Delete |

FastAPI uses these HTTP operations as path operations; the conventional REST mapping is POST=create, GET=read, PUT=update, and DELETE=delete.

# 3. REST

This is where students often get confused.

Tell them:

**REST is not a programming language, framework, or library.**

REST is an architectural style for designing APIs around resources and HTTP operations.

For example, consider students.

Bad conceptual design:

/getAllStudents
/createStudent
/updateStudent
/deleteStudent

REST-style design:

GET    /students
POST   /students
GET    /students/101
PUT    /students/101
DELETE /students/101

# 4. Status Codes

Teach only the important ones initially.

2xx — Success
200 → OK
201 → Created
204 → No Content
4xx — Client Error
400 → Bad Request
401 → Unauthorized
403 → Forbidden
404 → Not Found
5xx — Server Error
500 → Internal Server Error

FastAPI documents 200 as the normal successful response, 201 as commonly used after creating a resource, 204 as no-content, and 404 as not-found

# 5. JSON

Students should understand why JSON is everywhere in APIs.

Example:

{
    "id": 101,
    "name": "Ravi",
    "course": "Data Science",
    "active": true
}

Explain:

Python dictionary
       ↓
      JSON
       ↓
JavaScript / Browser / Mobile App / Other API

Important distinction:

**Python dictionary**
student = {
    "name": "Ravi",
    "age": 25
}

versus:

{
    "name": "Ravi",
    "age": 25
}

# 6. Day 1 Practical — JSONPlaceholder

JSONPlaceholder is a public fake REST API specifically intended for testing, tutorials, prototypes, and examples, and it requires no signup or API key.

We will use:

https://jsonplaceholder.typicode.com