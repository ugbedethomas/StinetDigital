# project_status.py
import os
import django
import sys

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stinet_core.settings')
django.setup()

from talent.models import *
from academy.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


def print_status():
    print("📊 STINET DIGITAL ERP - PROJECT STATUS")
    print("=" * 50)

    print("\n👥 USERS MODULE:")
    print(f"   Total users: {User.objects.count()}")
    for role in ['STUDENT', 'CLIENT', 'TRAINER', 'ADMIN', 'SUPER_ADMIN']:
        count = User.objects.filter(role=role).count()
        if count > 0:
            print(f"   - {role}: {count}")

    print("\n🎓 ACADEMY MODULE:")
    print(f"   Courses: {Course.objects.count()}")
    print(f"   Enrollments: {Enrollment.objects.count()}")

    print("\n💼 TALENT PIPELINE MODULE:")
    print(f"   Portfolios: {Portfolio.objects.count()}")
    print(f"   Skills: {Skill.objects.count()}")
    print(f"   Companies: {Company.objects.count()}")
    print(f"   Active Jobs: {JobPosting.objects.filter(is_active=True).count()}")
    print(f"   Applications: {Application.objects.count()}")
    print(f"   Placements: {Placement.objects.count()}")

    print("\n🔗 API ENDPOINTS (Port 8001):")
    print("   http://127.0.0.1:8001/admin/")
    print("   http://127.0.0.1:8001/api/talent/test/")
    print("   http://127.0.0.1:8001/api/academy/courses/")
    print("   http://127.0.0.1:8001/api/auth/login/")

    print("\n✅ PHASE COMPLETION:")
    print("   Phase 1: Authentication - ✅ 100%")
    print("   Phase 2: Academy - ✅ 100%")
    print("   Phase 3: Talent Pipeline - 🚧 70%")
    print("   Phase 4: Client Hub - 🚧 0%")
    print("   Phase 5: Frontend - 🚧 0%")

    print("\n🎯 NEXT STEPS FOR PHASE 3:")
    print("   1. Create REST API endpoints for Talent models")
    print("   2. Implement job matching algorithm")
    print("   3. Build company portal views")
    print("   4. Create student portfolio management")
    print("   5. Write tests for Talent module")


if __name__ == "__main__":
    print_status()