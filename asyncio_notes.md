# Python `asyncio`, `async`, and `await`

## 1. What is `asyncio`?

`asyncio` is Python's standard-library framework for writing concurrent programs with `async` and `await`. It is especially useful when a program spends time waiting for network responses, database queries, files, timers, or other I/O.

With ordinary blocking code, one operation waits until it finishes before the next operation starts. With asynchronous code, a task can pause while it waits for I/O, allowing the event loop to run another task during that time.

Typical uses include:

- Making several HTTP requests without waiting for each one in sequence.
- Serving many network connections efficiently.
- Waiting for asynchronous database operations.
- Running timers and background tasks alongside I/O work.

`asyncio` is not automatically faster for every program. It is most helpful when there is a lot of waiting. CPU-heavy work generally needs a process pool, a thread pool, or a different approach.

## 2. The main ideas

### Coroutine function

A function declared with `async def` is an asynchronous function, also called a coroutine function:

```python
async def get_message():
    return "Hello"
```

Calling it does not immediately run its body and does not directly return the string. It creates a coroutine object:

```python
coroutine = get_message()
```

That coroutine must be awaited or scheduled as a task. Otherwise, it will not run, and Python may warn that the coroutine was never awaited.

### Coroutine

A coroutine is the object produced by calling an `async def` function. It describes asynchronous work that can be run and awaited.

### Event loop

The event loop coordinates asynchronous work. It runs tasks, tracks what each task is waiting for, and resumes tasks when their awaited operation is ready.

In ordinary `asyncio` programs, you usually start the event loop once with:

```python
asyncio.run(main())
```

`asyncio.run()` creates and manages the loop for the program's top-level asynchronous entry point. Do not call it from inside an already-running event loop. Frameworks such as FastAPI and notebook environments may already be running one.

### Task

A task wraps a coroutine and schedules it to run on the event loop. Use `asyncio.create_task()` when you want work to begin running concurrently with other work:

```python
task = asyncio.create_task(do_work())
result = await task
```

Creating a task schedules it; it does not create a new operating-system thread. Keep a reference to tasks you start and make sure their results or exceptions are handled.

### Awaitable

An awaitable is an object that can be used with `await`. Coroutines, tasks, and futures are common awaitables.

## 3. What `async` and `await` mean

### `async def`

`async def` declares a coroutine function. It allows the function to use `await` in its body:

```python
async def fetch_data():
    data = await some_async_operation()
    return data
```

### `await`

`await` says: wait for this awaitable's result. While the current task is waiting, the event loop can run other tasks that are ready.

```python
result = await some_async_operation()
```

`await` does not mean "run this in another thread." It pauses the current coroutine at that point and gives the event loop an opportunity to do other work. If the awaited operation completes immediately, the task may continue without a noticeable pause.

You can only use `await` inside an `async def` function (apart from specialized interactive environments that support top-level await).

## 4. Concurrency versus parallelism

- **Concurrency** means multiple tasks make progress over overlapping periods. An event loop can switch between tasks while they wait.
- **Parallelism** means multiple operations execute at the exact same time, usually on different CPU cores or threads.

`asyncio` primarily provides concurrency on an event loop. It is excellent for overlapping I/O waits, but it does not make ordinary CPU calculations execute in parallel by itself.

## 5. Blocking and non-blocking waits

This blocks the thread and prevents the event loop from doing other work on that thread:

```python
import time

time.sleep(2)
```

This is an asynchronous wait. It suspends the current task and lets other tasks run:

```python
import asyncio

await asyncio.sleep(2)
```

Inside asynchronous code, use asynchronous versions of I/O operations. Calling a blocking HTTP client, database driver, or `time.sleep()` from an async function can stall every other task sharing that event loop.

## 6. Your coffee-and-tea example

In `async_await.py`, both functions pause with `await asyncio.sleep(...)`. The main function creates both tasks before awaiting either one:

```python
coffee_task = asyncio.create_task(coffee_async())
tea_task = asyncio.create_task(tea_async())

coffee_result = await coffee_task
tea_result = await tea_task
```

Both tasks are scheduled before the first `await`. While coffee is sleeping, tea can also make progress, and vice versa. With waits of 2 seconds and 3 seconds, total time is approximately 3 seconds, not 5 seconds. The tasks overlap; the total is close to the longest wait, plus small overhead.

If instead you awaited each coroutine directly, one after the other, their waits would be sequential:

```python
coffee_result = await coffee_async()
tea_result = await tea_async()
```

That takes approximately 5 seconds. `await` alone does not make two operations concurrent; concurrency requires scheduling multiple operations so they can overlap.

Your current functions print a "ready" message and also return that same message. Then `main_async()` prints each returned value. That is why each ready message appears twice: once from inside the function and once from printing its result.

## 7. A concise concurrent example

`asyncio.gather()` runs multiple awaitables concurrently and returns results in the same order as the arguments:

```python
import asyncio
from time import perf_counter


async def coffee():
    await asyncio.sleep(2)
    return "Coffee is ready!"


async def tea():
    await asyncio.sleep(3)
    return "Tea is ready!"


async def main():
    start = perf_counter()
    coffee_result, tea_result = await asyncio.gather(coffee(), tea())
    elapsed = perf_counter() - start

    print(coffee_result)
    print(tea_result)
    print(f"Total time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
```

Use `time.perf_counter()` for measuring elapsed time. It is designed for duration measurements; `time.time()` represents wall-clock time and can change when the system clock is adjusted.

`asyncio.gather()` is convenient when you know the set of operations to run together. If one operation raises an exception, `gather()` propagates that exception by default. Other submitted operations are not automatically cancelled simply because that exception was propagated, so consider how you want errors and remaining work handled.

## 8. Choosing between direct `await`, tasks, and `gather`

- Use **direct `await`** when the next step depends on the previous result, or when you intentionally want sequential work.
- Use **`asyncio.create_task()`** to schedule work early so it can overlap with other work. Await the task later to collect its result.
- Use **`asyncio.gather()`** to run a known group of awaitables concurrently and collect their results together.
- In Python 3.11+, use **`asyncio.TaskGroup`** when you want structured task management: tasks are scoped to a block and the block waits for them to finish.

Example of dependent sequential steps:

```python
user = await fetch_user()
orders = await fetch_orders(user.id)
```

Example of independent work that can overlap:

```python
user_task = asyncio.create_task(fetch_user())
settings_task = asyncio.create_task(fetch_settings())

user = await user_task
settings = await settings_task
```

## 9. Common mistakes

### Calling an async function without awaiting or scheduling it

```python
result = fetch_data()  # This is a coroutine object, not the result.
```

Instead, use `await fetch_data()` inside async code, or schedule it with `asyncio.create_task()` when it should run concurrently.

### Expecting `await` by itself to create concurrency

```python
first = await first_request()
second = await second_request()
```

This is sequential. Schedule independent operations together with `gather()` or tasks.

### Using blocking functions inside async code

`time.sleep()`, synchronous network clients, and blocking database calls can freeze the event loop. Use async-compatible APIs, or deliberately move blocking work to a thread/process executor where appropriate.

### Creating tasks and forgetting them

An untracked task can fail without its exception being handled, or the program can finish before the work is complete. Keep task references and await them, or use structured concurrency such as `TaskGroup`.

### Trying to use `asyncio.run()` inside a running loop

Call `asyncio.run()` at a normal program's synchronous entry point. In an async framework handler, await asynchronous functions directly; do not start a second event loop with `asyncio.run()`.

### Making CPU-heavy work `async` and expecting it to speed up

Declaring a function `async` does not make CPU work non-blocking. A long calculation with no `await` still occupies the event-loop thread. Use an appropriate process pool or other CPU parallelism when needed.

## 10. Errors, cancellation, and timeouts

An exception raised by an awaited coroutine is raised at the `await` expression. Use normal `try`/`except` around the await:

```python
try:
    result = await fetch_data()
except OSError as error:
    print(f"Network operation failed: {error}")
```

Tasks can be cancelled. Cancellation is cooperative: the task receives `asyncio.CancelledError` at an await point, giving it a chance to clean up. Use `finally` for cleanup and normally re-raise `CancelledError` after cleanup rather than swallowing it.

For a timeout, Python 3.11+ provides `asyncio.timeout()`:

```python
async with asyncio.timeout(5):
    result = await fetch_data()
```

`asyncio.wait_for(awaitable, timeout=5)` is another commonly used timeout API. Choose based on the Python version and the cancellation behavior you need.

## 11. How this relates to FastAPI

FastAPI supports both regular `def` and `async def` path operations:

```python
@app.get("/items")
async def get_items():
    items = await async_database_call()
    return items
```

Use `async def` when the code calls async-compatible libraries and needs to await their operations. A blocking call made directly inside an async route blocks the event loop and can delay unrelated requests. If a library only offers blocking operations, use a synchronous route or move that blocking work off the event loop as appropriate.

Marking a route `async def` does not make its database or HTTP client asynchronous. The libraries used inside the route must provide non-blocking async operations for the route to benefit from `await`.

## 12. Quick reference

| Syntax/API | Purpose |
|---|---|
| `async def function()` | Declare a coroutine function |
| `await operation()` | Wait for an awaitable and let the loop run other work |
| `asyncio.run(main())` | Start and manage the top-level event loop |
| `asyncio.create_task(coro())` | Schedule a coroutine to run concurrently |
| `await asyncio.gather(a(), b())` | Run a group of awaitables concurrently and collect results |
| `await asyncio.sleep(seconds)` | Wait without blocking the event-loop thread |
| `time.sleep(seconds)` | Blocking sleep; avoid inside async code |
| `time.perf_counter()` | Measure elapsed duration |

## Key takeaway

`async` defines asynchronous functions, `await` pauses one coroutine while an awaitable completes, and `asyncio`'s event loop coordinates tasks so other work can proceed during waits. The biggest practical rule is: use non-blocking async operations in code running on the event loop, and schedule independent work together when it should overlap.