# demo_talent_data.py
import os
import django
import sys

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stinet_core.settings')
django.setup()

from talent.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


def show_demo_data():
    print("🎓 STINET TALENT PIPELINE - DEMO DATA")
    print("======================================")

    # Users
    users = User.objects.all()
    print(f"\n👥 USERS ({users.count()} total):")
    for role in ['STUDENT', 'CLIENT', 'TRAINER', 'ADMIN', 'SUPER_ADMIN']:
        count = User.objects.filter(role=role).count()
        if count > 0:
            print(f"  {role}: {count}")

    # Portfolios
    portfolios = Portfolio.objects.all()
    print(f"\n💼 PORTFOLIOS ({portfolios.count()}):")
    for p in portfolios[:3]:  # Show first 3
        print(f"  - {p.student.username}: {p.title}")
    if portfolios.count() > 3:
        print(f"  ... and {portfolios.count() - 3} more")

    # Jobs
    jobs = JobPosting.objects.filter(is_active=True)
    print(f"\n📋 ACTIVE JOBS ({jobs.count()}):")
    for job in jobs[:3]:
        print(f"  - {job.title} at {job.company.name}")
        skills = [s.name for s in job.skills_required.all()[:3]]
        if skills:
            print(f"    Skills: {', '.join(skills)}")
    if jobs.count() > 3:
        print(f"  ... and {jobs.count() - 3} more")

    # Skills
    skills = Skill.objects.all()
    print(f"\n🛠️ SKILLS ({skills.count()}):")
    skill_categories = {}
    for skill in skills:
        if skill.category not in skill_categories:
            skill_categories[skill.category] = []
        skill_categories[skill.category].append(skill.name)

    for category, skill_list in list(skill_categories.items())[:3]:
        print(f"  {category}: {', '.join(skill_list[:5])}")
        if len(skill_list) > 5:
            print(f"    ... and {len(skill_list) - 5} more")

    print("\n🔗 API ENDPOINTS AVAILABLE:")
    print("  GET /api/talent/test/")
    print("  GET /api/talent/api/jobs/")
    print("  GET /api/talent/api/skills/")
    print("  GET /api/talent/api/portfolios/")
    print("  GET /api/talent/api/companies/")

    print("\n🎉 PHASE 3 COMPLETE - READY FOR PHASE 4!")


if __name__ == '__main__':
    show_demo_data()