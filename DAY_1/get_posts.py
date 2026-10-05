import requests


url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url)

print("Status Code:", response.status_code)

data = response.json()

print("Total Posts:", len(data))

for post in data[:5]:
    print(post)



#=======================================
#        POST Request Example
#=======================================
import requests


url = "https://jsonplaceholder.typicode.com/posts"

data = {
    "title": "FastAPI Training",
    "body": "Learning REST APIs",
    "userId": 1
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)

print("Response:")
print(response.json())