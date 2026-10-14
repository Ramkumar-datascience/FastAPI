#### install required libraries

python -m pip install fastapi uvicorn sqlalchemy "pwdlib[argon2]" PyJWT python-multipart cachetools

### How to run the application?
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
python -m uvicorn main:app --reload

### Test it step by step

1. Login: Open POST /login, click Try it out, and enter username admin and password Admin@12345. The login endpoint accepts form data, not JSON.
2. Authorize: Copy the access_token from the response. Click Authorize in Swagger and enter the token as a Bearer token. Depending on the Swagger prompt, paste just the token, not the word Bearer.
3. Create: Use POST /students/ with this JSON:
   json     {       "name": "Ram",       "email": "ram@example.com"     }
4. Read: Use GET /students/ to list students.
5. Update: Use PUT /students/1 with the updated name and email, using the actual ID returned by the create request.
6. Delete: Use DELETE /students/1 with the appropriate student ID.