
from fastapi import FastAPI
from functools import lru_cache
import time

app = FastAPI()

# This function's result will be cached
@lru_cache(maxsize=10)
def get_student(student_id: int):
    print("Fetching data...")

    # Simulate a slow database operation
    time.sleep(3)

    return {
        "id": student_id,
        "name": "Ram"
    }

@app.get("/student/{student_id}")
def student(student_id: int):
    return get_student(student_id)


# @lru_cache stores function results in memory.
# maxsize=10 keeps up to 10 recent argument/result combinations.
# The cache disappears when the application process restarts.