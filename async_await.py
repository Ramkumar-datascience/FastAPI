import time
import asyncio

# def coffee():
#     print("Coffee is brewing...")
#     time.sleep(2)
#     print("Coffee is ready!")
#     return "Coffee is ready!"

# def tea():
#     print("Tea is brewing...")
#     time.sleep(3)
#     print("Tea is ready!")
#     return "Tea is ready!"

# def main():
#     start_time = time.time()

#     coffee_result = coffee()
#     tea_result = tea()

#     end_time = time.time()
#     elapsed_time = end_time - start_time

#     print(coffee_result)
#     print(tea_result)
#     print(f"Total time taken: {elapsed_time:.2f} seconds")

# if __name__ == "__main__":
#     main()

#==================================================
# Let's make it asynchronous using async/await
#==================================================

async def coffee_async():
    print("Coffee is brewing...")
    await asyncio.sleep(2)
    print("Coffee is ready!")
    return "Coffee is ready!"

async def tea_async():
    print("Tea is brewing...")
    await asyncio.sleep(3)
    print("Tea is ready!")
    return "Tea is ready!"

async def main_async():
    start_time = time.time()

    coffee_task = asyncio.create_task(coffee_async())
    tea_task = asyncio.create_task(tea_async())

    coffee_result = await coffee_task
    tea_result = await tea_task

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(coffee_result)
    print(tea_result)
    print(f"Total time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main_async())