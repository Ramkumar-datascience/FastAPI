from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Database dependency
from db_connection import get_db

# SQLAlchemy Student model
from models import Student

# Pydantic schemas
from schema import StudentCreate, StudentResponse

# =========================================================
# CREATE FASTAPI APPLICATION
# =========================================================

# We are creating the FastAPI application here itself.
#
# Since we are NOT using APIRouter,
# all our API routes will be directly created using "app".
app = FastAPI(title="Student Management API")

# =========================================================
# CREATE STUDENT
# =========================================================

@app.post("/students/",response_model=StudentResponse)
def create_student(student: StudentCreate,

    # FastAPI gets a database session automatically
    # from the get_db() function.
    db: Session = Depends(get_db)):

    # Convert Pydantic object into SQLAlchemy object
    
    db_student = Student(
        name=student.name,
        email=student.email,
        course=student.course
    )

    db.add(db_student)
    # Save the changes permanently
    db.commit()

    # -----------------------------------------------------
    # Refresh the object
    # -----------------------------------------------------
    # SQLite generates the ID automatically.
    # refresh() gets the newly generated ID.    
    db.refresh(db_student)

    # Return the newly created student
    return db_student

@app.get("/students/",response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):

    # Query all students from the database
    students = db.query(Student).all()

    return students

@app.get("/students/{student_id}",response_model=StudentResponse)
def get_student(student_id: int,db: Session = Depends(get_db)):

    # Search for the student using the ID
    student = (
        db.query(Student)
        .filter(Student.id == student_id).first()
    )

    # -----------------------------------------------------
    # If student doesn't exist
    # -----------------------------------------------------

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return student

# =========================================================
# UPDATE STUDENT
# =========================================================

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(student_id: int,
    # New student data coming from the client
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Find existing student
    # -----------------------------------------------------

    db_student = (
        db.query(Student)
        .filter(Student.id == student_id).first()
    )

    # -----------------------------------------------------
    # Student doesn't exist
    # -----------------------------------------------------

    if db_student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # -----------------------------------------------------
    # Update the existing values
    # -----------------------------------------------------

    db_student.name = student_data.name
    db_student.email = student_data.email
    db_student.course = student_data.course

    # -----------------------------------------------------
    # Save changes
    # -----------------------------------------------------

    db.commit()

    # Get the updated database object
    db.refresh(db_student)

    return db_student

# =========================================================
# DELETE STUDENT
# =========================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):

    # -----------------------------------------------------
    # Find student
    # -----------------------------------------------------

    db_student = (
        db.query(Student)
        .filter(Student.id == student_id).first()
    )

    # -----------------------------------------------------
    # Student doesn't exist
    # -----------------------------------------------------

    if db_student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # -----------------------------------------------------
    # Delete student
    # -----------------------------------------------------

    db.delete(db_student)

    # Save deletion
    db.commit()

    return {
        "message": "Student deleted successfully"
    }