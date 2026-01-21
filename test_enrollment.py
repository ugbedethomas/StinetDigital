import requests
import json

BASE_URL = "http://127.0.0.1:8001/api"


def test_enrollment_system():
    print("🧪 Testing Enrollment System...")
    print("=" * 60)

    # 1. Login as student
    print("\n1. Logging in as student...")
    response = requests.post(f"{BASE_URL}/auth/login/", json={
        "username": "python.test",
        "password": "Test123!"
    })

    if response.status_code != 200:
        print("❌ Login failed. Creating test student...")
        # Create test student first
        requests.post(f"{BASE_URL}/auth/register/", json={
            "username": "test.student",
            "password": "student123",
            "password2": "student123",
            "role": "STUDENT"
        })
        response = requests.post(f"{BASE_URL}/auth/login/", json={
            "username": "test.student",
            "password": "student123"
        })

    token_data = response.json()
    access_token = token_data['tokens']['access']
    headers = {'Authorization': f'Bearer {access_token}'}
    print(f"✅ Logged in as: {token_data['user']['username']}")

    # 2. Get available courses
    print("\n2. Fetching available courses...")
    response = requests.get(f"{BASE_URL}/academy/courses/")
    courses = response.json()
    print(f"✅ Found {len(courses)} courses")

    if courses:
        course_id = courses[0]['id']
        print(f"   First course: {courses[0]['title']} (ID: {course_id})")

        # 3. Enroll in course
        print("\n3. Enrolling in course...")
        response = requests.post(
            f"{BASE_URL}/academy/enroll/",
            json={"course_id": course_id},
            headers=headers
        )

        # After enrollment, get the enrollment ID properly
        if response.status_code == 201:
            print("✅ Successfully enrolled!")
            enrollment_data = response.json()

            # Get enrollment ID from response
            if 'enrollment' in enrollment_data:
                enrollment_id = enrollment_data['enrollment']['id']
            elif 'id' in enrollment_data:
                enrollment_id = enrollment_data['id']
            else:
                # If no ID in response, get it from dashboard
                print("   Getting enrollment ID from dashboard...")
                dash_response = requests.get(f"{BASE_URL}/academy/dashboard/", headers=headers)
                if dash_response.status_code == 200:
                    dashboard = dash_response.json()
                    if dashboard['enrollments']:
                        enrollment_id = dashboard['enrollments'][0]['id']
                    else:
                        print("   ❌ No enrollments found in dashboard")
                        enrollment_id = None
                else:
                    enrollment_id = None