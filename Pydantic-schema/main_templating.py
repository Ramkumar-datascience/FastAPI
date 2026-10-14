# lets create a fastapi application with pydantic schema and jinja2 templating
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schema import UserSchema
from main import students

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request,"home.html")

@app.get("/students", response_class=HTMLResponse)
def get_students(request: Request):
    return templates.TemplateResponse(request,"students.html", {"students": students})

@app.post("/students", response_class=HTMLResponse)
def create_student(request: Request, student: UserSchema):
    new_student = student.dict()
    new_student["id"] = len(students) + 1
    students.append(new_student)
    return templates.TemplateResponse(request,"students.html", {"students": students})

@app.post("/add-student", response_class=HTMLResponse)
def add_student(request: Request):
    return templates.TemplateResponse(request,"add_student.html")