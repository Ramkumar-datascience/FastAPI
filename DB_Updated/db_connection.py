# Database connection file
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# 1. SQLite Database URL
# ---------------------------------------------------------
# sqlite:///./students.db means:
#
# sqlite  -> We are using SQLite
# ./      -> Current folder
# students.db -> Database file name
#
# So students.db will be created in this project folder.
DATABASE_URL = "sqlite:///./students.db"

# ---------------------------------------------------------
# 2. Create SQLAlchemy Engine
# ---------------------------------------------------------
# Engine is responsible for communicating with the database.
engine = create_engine(
    DATABASE_URL,

    # SQLite normally restricts a connection to one thread.
    # FastAPI can work with multiple threads,
    # so we disable this SQLite restriction.
    connect_args={"check_same_thread": False}
)

# ---------------------------------------------------------
# 3. Create Database Session
# ---------------------------------------------------------
# SessionLocal will be used whenever we want to
# communicate with the database.
#
# Think of a Session as a temporary connection/workspace
# for performing database operations.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------------------------
# 4. Base Class
# ---------------------------------------------------------
# All our SQLAlchemy models will inherit from this Base.
#
# Example:
# class Student(Base):
#     ...
Base = declarative_base()

# ---------------------------------------------------------
# 5. Database Dependency
# ---------------------------------------------------------
# FastAPI will use this function to create a database
# session for each API request.
#
# We will use it with Depends() in our router.
def get_db():

    db = SessionLocal()

    try:
        # Give the database session to the API
        yield db

    finally:
        # Always close the database connection
        # after the API request is completed.
        db.close()