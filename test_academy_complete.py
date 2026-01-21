import requests
import json

BASE_URL = "http://127.0.0.1:8001/api"


def print_test_result(test_name, success, details=""):
    icon = "✅" if success else "❌"
    print(f"{icon} {test_name}")
    if details:
        print(f"   {details}")


def test_complete_academy():
    print("🎓 COMPLETE ACADEMY SYSTEM TEST")
    print("=" * 60)

    results = []

    # 1. Test public endpoints
    print("\n1. Testing Public Endpoints:")

    # Test endpoint
    response = requests.get(f"{BASE_URL}/academy/test/")
    results.append(("API Test", response.status_code == 200, f"Status: {response.status_code}"))

    # Categories
    response = requests.get(f"{BASE_URL}/academy/categories/")
    results.append(("Categories", response.status_code == 200, f"Count: {len(response.json())}"))

    # Courses
    response = requests.get(f"{BASE_URL}/academy/courses/")
    courses = response.json()
    results.append(("Courses", response.status_code == 200, f"Count: {len(courses)}"))

    # 2. Test authentication and enrollment
    print("\n2. Testing Authentication & Enrollment:")

    # Login or create student
    login_data = {"username": "academy.test", "password": "test123"}
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)

    if response.status_code != 200:
        # Create student
        requests.post(f"{BASE_URL}/auth/register/", json={
            "username": "academy.test",
            "password": "test123",
            "password2": "test123",
            "role": "STUDENT"
        })
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['tokens']['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        results.append(("Login", True, f"User: {token_data['user']['username']}"))

        # Enroll in first course
        if courses:
            course_id = courses[0]['id']
            enroll_response = requests.post(
                f"{BASE_URL}/academy/enroll/",
                json={"course_id": course_id},
                headers=headers
            )
            results.append(("Enrollment", enroll_response.status_code == 201, f"Status: {enroll_response.status_code}"))

            # Test dashboard
            dash_response = requests.get(f"{BASE_URL}/academy/dashboard/", headers=headers)
            if dash_response.status_code == 200:
                dashboard = dash_response.json()
                results.append(("Dashboard", True, f"Courses: {dashboard['statistics']['total_courses']}"))

                # Test progress update if we have enrollment
                if dashboard['enrollments']:
                    enrollment_id = dashboard['enrollments'][0]['id']
                    progress_response = requests.post(
                        f"{BASE_URL}/academy/enrollments/{enrollment_id}/progress/",
                        json={"progress": 75},
                        headers=headers
                    )
                    results.append(("Progress Update", progress_response.status_code == 200,
                                    f"Status: {progress_response.status_code}"))
    else:
        results.append(("Login", False, f"Status: {response.status_code}"))

    # 3. Print results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    for test_name, success, details in results:
        print_test_result(test_name, success, details)
        if success:
            passed += 1

    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    print("=" * 60)

    return passed == len(results)


if __name__ == "__main__":
    test_complete_academy()