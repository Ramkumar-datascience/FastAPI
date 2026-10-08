# this is our main FastAPI application
from fastapi import FastAPI

# Import database Base and engine
from db_connection import Base, engine

# Import student router
from routers.students import router as student_router

# =========================================================
# Create Database Tables
# =========================================================
# This checks whether the tables defined in our
# SQLAlchemy models exist.
#
# If they don't exist, SQLAlchemy creates them.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    description="Simple FastAPI + SQLite + SQLAlchemy CRUD API",
    version="1.0"
)

# Include the student router
app.include_router(student_router)

@app.get("/")
def home():

    return {
        "message": "Student Management API is running"
    }