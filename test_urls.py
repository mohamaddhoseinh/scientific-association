import requests

# تست API Root
try:
    response = requests.get('http://127.0.0.1:8000/api/')
    print(f"API Root Status: {response.status_code}")
    print(f"Content: {response.text[:200]}...")
except Exception as e:
    print(f"API Root Error: {e}")

# تست Swagger
try:
    response = requests.get('http://127.0.0.1:8000/swagger/')
    print(f"Swagger Status: {response.status_code}")
    if response.status_code == 200:
        print("Swagger is working!")
    else:
        print(f"Swagger Error: {response.text[:200]}...")
except Exception as e:
    print(f"Swagger Error: {e}")