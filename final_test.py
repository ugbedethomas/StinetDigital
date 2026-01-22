# final_test.py
import os
import sys

print("=" * 60)
print("FINAL STINET ERP SYSTEM TEST")
print("=" * 60)

# Set up Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stinet_core.settings')

try:
    # Import Django
    import django

    django.setup()
    print("[PASS] Django setup successful")

    print("\n--- Testing Models ---")

    # Test User model
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user_count = User.objects.count()
    print(f"[PASS] User model: {user_count} users")

    # Test Talent models
    from talent.models import Portfolio, JobPosting, Skill, Company

    print(f"[PASS] Portfolio model: {Portfolio.objects.count()} portfolios")
    print(f"[PASS] JobPosting model: {JobPosting.objects.filter(is_active=True).count()} active jobs")
    print(f"[PASS] Skill model: {Skill.objects.count()} skills")
    print(f"[PASS] Company model: {Company.objects.count()} companies")

    # Test Academy models
    from academy.models import Course, Enrollment

    print(f"[PASS] Course model: {Course.objects.count()} courses")
    print(f"[PASS] Enrollment model: {Enrollment.objects.count()} enrollments")

    print("\n--- Testing API Endpoints ---")

    # Check URL configuration
    from django.urls import get_resolver

    resolver = get_resolver()
    url_count = len([p for p in resolver.url_patterns if hasattr(p, 'name')])
    print(f"[PASS] URL patterns: {url_count} routes configured")

    # Check talent URLs
    from talent import urls as talent_urls

    talent_route_count = len(talent_urls.urlpatterns)
    print(f"[PASS] Talent URLs: {talent_route_count} routes")

    print("\n" + "=" * 60)
    print("SYSTEM STATUS: OPERATIONAL")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start server: python manage.py runserver 8001")
    print("2. Test endpoints:")
    print("   - http://127.0.0.1:8001/api/talent/test/")
    print("   - http://127.0.0.1:8001/api/talent/api/jobs/")
    print("   - http://127.0.0.1:8001/admin/")
    print("3. Create superuser if needed: python manage.py createsuperuser")

except Exception as e:
    print(f"\n[FAIL] System test failed: {type(e).__name__}")
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()

    print("\n" + "=" * 60)
    print("SYSTEM STATUS: NEEDS ATTENTION")
    print("=" * 60)