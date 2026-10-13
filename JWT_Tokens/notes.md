### required libraries

python -m pip install fastapi uvicorn PyJWT "pwdlib[argon2]" python-multipart

## step-1 create a JWT Token before run the application

1. $env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
2. python -m uvicorn app:app --reload

## Steps to run the application
1. http://127.0.0.1:8000/docs
2. Try Open GET /public
3. Login and generate a token
    - Open POST /token
    - Username : ram
    - Password : learnfastapi123
4. Access the protected endpoint
    - Open GET /profile
    - Click Authorize in Swagger(top right corner).
    - Enter the username and password when prompted, if Swagger has not already obtained a token.
    - Authorize and close the dialog.
    - Execute GET /profile