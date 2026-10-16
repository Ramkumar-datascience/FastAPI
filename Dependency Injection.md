## 1. What is Dependency Injection?
Imagine you are teaching a Python class. Whenever you enter the classroom, you need a laptop, a projector, and a marker.
Instead of arranging these things yourself every time, someone provides them to you before the class starts.

That is the basic idea of Dependency Injection (DI).
- Dependency: Something your function needs to do its job.
- Injection: Providing that required thing to the function automatically.

In Python, imagine this:

`def teach_class(laptop, projector):`
    `print("Teaching with laptop and projector")`

The function needs a laptop and projector. Someone must provide them.
In FastAPI, the framework can provide these dependencies for you.

## 2. What is Depends() in FastAPI?
Depends() is a FastAPI function that tells FastAPI:
**"Before executing this endpoint, call the required dependency and provide its result to my function."**
Let's understand this with a simple example

#### Without dependency injection
```
from fastapi import FastAPI

app = FastAPI()


def get_student():
    return {"name": "Ram", "course": "Data Science"}


@app.get("/student")
def student():
    data = get_student()
    return data
```
#### With dependency injection
```
from fastapi import FastAPI, Depends

app = FastAPI()


def get_student():
    return {"name": "Ram", "course": "Data Science"}


@app.get("/student")
def student(data: dict = Depends(get_student)):
    return data
```
### A more practical example: Dependency with parameters
Suppose multiple API endpoints need to know the current user's role.
Instead of writing the same logic in every endpoint, create a dependency function.

```
from fastapi import FastAPI, Depends

app = FastAPI()


def get_current_role():
    return "admin"


@app.get("/dashboard")
def dashboard(role: str = Depends(get_current_role)):
    return {"message": f"Welcome, {role}"}


@app.get("/reports")
def reports(role: str = Depends(get_current_role)):
    return {"role": role, "report": "Sales report"}
```
### Where do we use Depends() in real applications?

`1. Authentication`
    - Check whether a user is logged in before allowing access to an endpoint.

`2. Database connections`
    - Provide a database session to endpoints that need to read or write data.

`3. Validation and shared logic`
    - Reuse common checks, such as validating a token or checking user permissions.

`4. Configuration`
    - Provide shared settings or services to multiple endpoints.

### Why use Depends() when I can call the function directly?
Yes, you can call the function directly. In simple cases, both approaches can produce the same output. But **Depends() provides additional features that become useful as your application grows.**

So why use Depends()?
Imagine you have 20 endpoints that need to check whether a user is authenticated.
- Without Depends(), you must remember to call the authentication function in every endpoint. 
- With Depends(), you can declare the dependency, and FastAPI handles executing it before the endpoint.

Depends() will not cache the output, it used Dependency cache not HTTP cache
**FastAPI caches a dependency's result within a single HTTP request, not across multiple HTTP requests. This is what dependancy cache**

```
from fastapi import FastAPI, Depends

app = FastAPI()

def get_student():
    print("Executing get_student()")
    return {"name": "Ram"}

@app.get("/details")
def details(
    student1: dict = Depends(get_student),
    student2: dict = Depends(get_student)
):
    return {
        "first": student1,
        "second": student2
    }
```
we can use the same Depends() multiple times in the one function, so that it will call once utilize many times(dependency caching is enabled by default).

If you want FastAPI to execute the dependency separately for each declaration, you can use:
```
student1: dict = Depends(get_student, use_cache=False)
student2: dict = Depends(get_student, use_cache=False)
```

**One last clarification: dependency caching is not the same as application caching**

