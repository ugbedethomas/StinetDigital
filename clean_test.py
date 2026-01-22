# clean_test.py - No emojis to avoid encoding issues
import os
import sys
import subprocess

print("=== Testing Django Setup ===")

# Set up Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stinet_core.settings')

try:
    import django

    django.setup()
    print("[OK] Django setup successful")

    # Test imports
    from django.contrib.auth import get_user_model

    User = get_user_model()
    print(f"[OK] User model: {User.objects.count()} users")

    from talent.models import Portfolio, JobPosting, Skill

    print(f"[OK] Talent models loaded")
    print(f"     Portfolios: {Portfolio.objects.count()}")
    print(f"     Jobs: {JobPosting.objects.filter(is_active=True).count()}")
    print(f"     Skills: {Skill.objects.count()}")

    from academy.models import Course, Enrollment

    print(f"[OK] Academy models loaded")
    print(f"     Courses: {Course.objects.count()}")
    print(f"     Enrollments: {Enrollment.objects.count()}")

    print("\n=== ALL SYSTEMS GO ===")
    print("\nYou can now run: python manage.py runserver 8001")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback

    traceback.print_exc()