import requests
import json

BASE_URL = "http://127.0.0.1:8001/api"


def test_endpoints():
    print("Testing Stinet Digital API...")

    # Test 1: Test endpoint
    print("\n1. Testing /test/ endpoint:")
    response = requests.get(f"{BASE_URL}/test/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")

    # Test 2: Register user
    print("\n2. Testing registration:")
    data = {
        "username": "python.test",
        "email": "python@stinet.digital",
        "password": "Python123!",
        "password2": "Python123!",
        "role": "STUDENT",
        "phone": "08055555555"
    }
    response = requests.post(f"{BASE_URL}/register/", json=data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")

    # Test 3: Test error case
    print("\n3. Testing password mismatch:")
    data["password2"] = "WrongPassword!"
    response = requests.post(f"{BASE_URL}/register/", json=data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")


if __name__ == "__main__":
    test_endpoints()