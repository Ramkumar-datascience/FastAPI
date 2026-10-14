# lets create a fastapi application with pydantic schema
from fastapi import FastAPI, HTTPException
from schema import UserSchema

app = FastAPI()

students = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "is_active": False
    },
    {
        "id": 3,
        "name": "Bob Johnson",
        "email": "bob.johnson@example.com",
        "is_active": True
    }
]

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    student = next((student for student in students if student["id"] == student_id), None)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/students")
def create_student(student: UserSchema):
    new_student = student.dict()
    new_student["id"] = len(students) + 1
    students.append(new_student)
    return new_student