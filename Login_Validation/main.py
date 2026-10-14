from datetime import datetime, timedelta, timezone
import os

import jwt
from jwt.exceptions import InvalidTokenError
from cachetools import TTLCache
from pwdlib import PasswordHash

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ---------------- DATABASE ----------------

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- DATABASE TABLES ----------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


Base.metadata.create_all(bind=engine)

# ---------------- SECURITY AND CACHE ----------------

app = FastAPI(title="Login, CRUD and Caching Demo")

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-only-secret-change-before-deployment"
)
ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Cache user details for 60 seconds, maximum 100 users.
# Never cache plain-text passwords.
user_cache = TTLCache(maxsize=100, ttl=60)


# Create a demo user if it doesn't already exist.
with SessionLocal() as db:
    demo_user = db.query(User).filter(
        User.username == "admin"
    ).first()

    if demo_user is None:
        db.add(
            User(
                username="admin",
                hashed_password=password_hash.hash("Admin@12345")
            )
        )
        db.commit()

# ---------------- LOGIN ----------------

@app.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == form.username
    ).first()

    if user is None or not password_hash.verify(
        form.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    # Cache only safe user details after successful login.
    user_cache[user.username] = {
        "id": user.id,
        "username": user.username
    }

    # Generate a token valid for 30 minutes.
    token = jwt.encode(
        {
            "sub": user.username,
            "exp": datetime.now(timezone.utc)
                   + timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ---------------- AUTHENTICATION ----------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=401, detail="Invalid token"
            )

    except InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Invalid or expired token"
        )

    # Check cache first.
    cached_user = user_cache.get(username)

    if cached_user is not None:
        print("✅ User retrieved from CACHE")
        return cached_user

    
    # If not in cache, retrieve from database
    print("🗄️ User retrieved from DATABASE")
    user = db.query(User).filter(
        User.username == username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401, detail="User not found"
        )

    user_data = {
        "id": user.id,
        "username": user.username
    }

    # Store details in cache for subsequent requests.
    user_cache[username] = user_data

    return user_data


@app.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    return current_user

# ---------------- STUDENT SCHEMAS ----------------

class StudentCreate(BaseModel):
    name: str
    email: str


class StudentUpdate(BaseModel):
    name: str
    email: str


class StudentOut(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

# ---------------- CREATE STUDENT ----------------

@app.post("/students/", response_model=StudentOut)
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    existing = db.query(Student).filter(
        Student.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=409, detail="Email already exists"
        )

    student = Student(name=data.name, email=data.email)
    db.add(student)
    db.commit()
    db.refresh(student)

    return student

# ---------------- READ STUDENTS ----------------

@app.get("/students/", response_model=list[StudentOut])
def get_students(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Student).all()


@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404, detail="Student not found"
        )

    return student

# ---------------- UPDATE STUDENT ----------------

@app.put("/students/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404, detail="Student not found"
        )

    email_owner = db.query(Student).filter(
        Student.email == data.email,
        Student.id != student_id
    ).first()

    if email_owner:
        raise HTTPException(
            status_code=409, detail="Email already exists"
        )

    student.name = data.name
    student.email = data.email

    db.commit()
    db.refresh(student)

    return student


# ---------------- DELETE STUDENT ----------------

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404, detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}