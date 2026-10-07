# lets include HTML files in fastapi using jinja2 templates
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# def home():
#     html_content = """
#     <html>
#         <head>
#             <title>Welcome to My FastAPI Application</title>
#         </head>
#         <body>
#             <h1>Welcome to My FastAPI Application</h1>
#             <p>This is a simple FastAPI application with HTML response.</p>
#         </body>
#     </html>
#     """
#     return html_content

# using jinja2templates
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")

# lets create list of students and display them in html page using jinja2 templates
@app.get("/students", response_class=HTMLResponse)
def students(request: Request):
    student_list = [
        {"name": "Alice", "age": 20},
        {"name": "Bob", "age": 22},
        {"name": "Charlie", "age": 21}
    ]
    return templates.TemplateResponse(request, "students.html", {"students": student_list})

# lets try to implement static files for reading images, css and js files in fastapi
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(request, "about.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)