# Lets keep all database operations in one place.

from sqlalchemy.orm import Session

from models import Student
from schema import StudentCreate

# =========================================================
# CREATE
# =========================================================

def create_student(
    db: Session,
    student: StudentCreate
):

    # Convert Pydantic data into SQLAlchemy object
    db_student = Student(
        name=student.name,
        email=student.email,
        course=student.course
    )

    # Add the object to the database session
    db.add(db_student)

    # Save the changes permanently
    db.commit()

    # Refresh the object
    # This allows us to get the generated ID.
    db.refresh(db_student)

    return db_student

# =========================================================
# READ - ALL STUDENTS
# =========================================================

def get_students(db: Session):

    # Query all students from the database
    return db.query(Student).all()

# =========================================================
# READ - ONE STUDENT
# =========================================================

def get_student(
    db: Session,
    student_id: int
):

    # Search for a student using ID
    return (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

# =========================================================
# UPDATE
# =========================================================

def update_student(
    db: Session,
    student_id: int,
    student_data: StudentCreate
):

    # First find the student
    db_student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    # If student doesn't exist
    if db_student is None:
        return None


    # Update the values
    db_student.name = student_data.name
    db_student.email = student_data.email
    db_student.course = student_data.course


    # Save changes
    db.commit()

    # Refresh object
    db.refresh(db_student)

    return db_student

# =========================================================
# DELETE
# =========================================================

def delete_student(
    db: Session,
    student_id: int
):

    # Find the student
    db_student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    # Student doesn't exist
    if db_student is None:
        return None


    # Delete student
    db.delete(db_student)

    # Save deletion
    db.commit()

    return db_student