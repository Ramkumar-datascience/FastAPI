from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Database dependency
from db_connection import get_db
# CRUD functions
import crud
# Pydantic schemas
from schema import StudentCreate, StudentResponse

# ---------------------------------------------------------
# Create Router
# ---------------------------------------------------------
router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# =========================================================
# CREATE STUDENT
# =========================================================

@router.post("/",response_model=StudentResponse)
def create_student(
    student: StudentCreate,

    # FastAPI automatically creates database session
    db: Session = Depends(get_db)
):

    return crud.create_student(db,student)


# =========================================================
# GET ALL STUDENTS
# =========================================================

@router.get("/",response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db)
):

    return crud.get_students(db)


# =========================================================
# GET ONE STUDENT
# =========================================================

@router.get("/{student_id}",response_model=StudentResponse)
def get_student(
    student_id: int,

    db: Session = Depends(get_db)
):

    student = crud.get_student(db,student_id)

    # Student not found
    if student is None:

        raise HTTPException(status_code=404,
            detail="Student not found")

    return student


# =========================================================
# UPDATE STUDENT
# =========================================================

@router.put("/{student_id}",response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentCreate,

    db: Session = Depends(get_db)
):

    student = crud.update_student(
        db,
        student_id,
        student_data
    )

    # Student not found
    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# =========================================================
# DELETE STUDENT
# =========================================================

@router.delete("/{student_id}")
def delete_student(
    student_id: int,

    db: Session = Depends(get_db)
):

    student = crud.delete_student(db,student_id)

    # Student not found
    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully"
    }