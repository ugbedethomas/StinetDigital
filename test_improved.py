import requests
import json

BASE_URL = "http://127.0.0.1:8001/api"


def print_test_result(name, passed, response=None):
    icon = "✅" if passed else "❌"
    print(f"{icon} {name}")
    if response:
        print(f"   Status: {response.status_code}")
        if response.text:
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response: {response.text[:200]}")


def run_tests():
    print("🧪 TESTING IMPROVED REGISTRATION SYSTEM")
    print("=" * 60)

    tests = []

    # Test 1: API health check
    print("\n1. API Health Check:")
    response = requests.get(f"{BASE_URL}/test/")
    tests.append(("API Health", response.status_code == 200, response))

    # Test 2: Register new user
    print("\n2. Register New User:")
    data = {
        "username": "new.student",
        "email": "new@stinet.digital",
        "password": "Password123!",
        "password2": "Password123!",
        "role": "STUDENT",
        "phone": "08011111111"
    }
    response = requests.post(f"{BASE_URL}/register/", json=data)
    tests.append(("Register Success", response.status_code == 201, response))

    # Test 3: Try duplicate username
    print("\n3. Duplicate Username Validation:")
    response = requests.post(f"{BASE_URL}/register/", json=data)
    tests.append(("Duplicate Username", response.status_code == 400, response))

    # Test 4: Password mismatch
    print("\n4. Password Mismatch Validation:")
    data = {
        "username": "another.user",
        "password": "Password123!",
        "password2": "Different456!"
    }
    response = requests.post(f"{BASE_URL}/register/", json=data)
    tests.append(("Password Mismatch", response.status_code == 400, response))

    # Test 5: Login with new user
    print("\n5. Login with New User:")
    if tests[1][1]:  # If registration was successful
        login_data = {
            "username": "new.student",
            "password": "Password123!"
        }
        response = requests.post(f"{BASE_URL}/login/", json=login_data)
        tests.append(("Login Success", response.status_code == 200, response))

        # Save token if login successful
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('tokens', {}).get('access')

            # Test 6: Protected profile endpoint
            print("\n6. Protected Profile Endpoint:")
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(f"{BASE_URL}/profile/", headers=headers)
            tests.append(("Profile Access", response.status_code == 200, response))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    passed = sum(1 for test in tests if test[1])
    total = len(tests)

    for i, (name, passed_test, response) in enumerate(tests, 1):
        icon = "✅" if passed_test else "❌"
        print(f"  {i}. {icon} {name}")

    print(f"\n🎯 Results: {passed}/{total} tests passed ({passed / total * 100:.0f}%)")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()