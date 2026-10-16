## 1. What is Dependency Injection?
Imagine you are teaching a Python class. Whenever you enter the classroom, you need a laptop, a projector, and a marker.
Instead of arranging these things yourself every time, someone provides them to you before the class starts.

That is the basic idea of Dependency Injection (DI).
- Dependency: Something your function needs to do its job.
- Injection: Providing that required thing to the function automatically.

In Python, imagine this:
```def teach_class(laptop, projector):  
    print("Teaching with laptop and projector")```

The function needs a laptop and projector. Someone must provide them.
In FastAPI, the framework can provide these dependencies for you.

## 2. What is Depends() in FastAPI?
Depends() is a FastAPI function that tells FastAPI:
**"Before executing this endpoint, call the required dependency and provide its result to my function."**
Let's understand this with a simple example

#### Without dependency injection
