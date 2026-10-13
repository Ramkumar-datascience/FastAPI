from datetime import datetime, timedelta, timezone
import os

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash

# =========================================================
# 1. APPLICATION AND SECURITY CONFIGURATION
# =========================================================

app = FastAPI(title="JWT Authentication Demo")

# For a classroom demo, set a secret in your environment.
# Never use a hard-coded or publicly shared secret in production.
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "Set the JWT_SECRET_KEY environment variable before starting."
    )

# JWT signing algorithm used by this demo.
ALGORITHM = "HS256"

# Access tokens will expire after 10 minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = 10

# pwdlib hashes passwords so we do not store plaintext passwords.
password_hash = PasswordHash.recommended()

# =========================================================
# 2. DEMO USER STORE
# =========================================================

# This is an in-memory example, not a real user database.
# In production, load users from a database.
#
# Demo login:
# username = ram
# password = learnfastapi123
#
# We store a HASH of the password, not the actual password.
fake_users_db = {
    "ram": {
        "username": "ram",
        "full_name": "Ram Kumar",
        "hashed_password": password_hash.hash("learnfastapi123"),
    }
}

# =========================================================
# 3. OAUTH2 BEARER TOKEN SCHEME
# =========================================================

# FastAPI uses this dependency to extract a Bearer token
# from the Authorization header.
#
# tokenUrl points to the endpoint that issues tokens.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# =========================================================
# 4. CREATE AN ACCESS TOKEN
# =========================================================

def create_access_token(username: str) -> str:

    # Set the token expiration time.
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # "sub" identifies the subject (here, the username).
    # "exp" specifies when the token expires.
    payload = {
        "sub": username,
        "exp": expires_at,
    }

    # Sign the payload and return the encoded JWT string.
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# =========================================================
# 5. LOGIN ENDPOINT: USERNAME + PASSWORD -> TOKEN
# =========================================================

@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    # Find the user by username.
    user = fake_users_db.get(form_data.username)

    # Always reject invalid usernames/passwords.
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the submitted password against the stored hash.
    if not password_hash.verify(
        form_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Credentials are valid: issue an access token.
    access_token = create_access_token(user["username"])

    # The token response uses the standard OAuth2 field names.
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

# =========================================================
# 6. VALIDATE THE TOKEN AND IDENTIFY THE CURRENT USER
# =========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    # This exception is raised if the token is invalid,
    # incorrectly signed, or expired.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Verify the signature and expiration.
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Retrieve the subject from the token.
        username = payload.get("sub")

        if not username:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    # Confirm that this user still exists.
    user = fake_users_db.get(username)

    if user is None:
        raise credentials_exception

    return user

# =========================================================
# 7. PUBLIC ENDPOINT
# =========================================================

@app.get("/public")
def public_page():

    # Anyone can access this endpoint without logging in.
    return {
        "message": "This is public information."
    }

# =========================================================
# 8. PROTECTED ENDPOINT
# =========================================================

@app.get("/profile")
def get_profile(
    # FastAPI validates the token through get_current_user().
    current_user: dict = Depends(get_current_user)
):

    # Only a request with a valid token reaches this point.
    return {
        "message": "Authentication successful!",
        "username": current_user["username"],
        "full_name": current_user["full_name"],
    }