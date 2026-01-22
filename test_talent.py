# test_talent.py
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stinet_core.settings')
django.setup()

from talent.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

print("🧪 TESTING TALENT MODULE MODELS")
print("================================")

# Test 1: Create a skill
try:
    skill, created = Skill.objects.get_or_create(
        name='Python',
        defaults={'category': 'Programming', 'icon': 'code'}
    )
    print(f"✅ Skill: {skill.name} ({'Created' if created else 'Exists'})")
except Exception as e:
    print(f"❌ Skill creation failed: {e}")

# Test 2: Get or create a student
try:
    student_user, created = User.objects.get_or_create(
        username='test_student',
        defaults={
            'email': 'student@test.com',
            'role': 'STUDENT'
        }
    )
    if created:
        student_user.set_password('testpass123')
        student_user.save()
    print(f"✅ Student user: {student_user.username} ({'Created' if created else 'Exists'})")
except Exception as e:
    print(f"❌ Student creation failed: {e}")

# Test 3: Create portfolio for student
try:
    if student_user.role == 'STUDENT':
        portfolio, created = Portfolio.objects.get_or_create(
            student=student_user,
            defaults={
                'title': f"{student_user.username}'s Portfolio",
                'bio': 'A talented developer portfolio',
                'is_public': True
            }
        )
        print(f"✅ Portfolio: {portfolio.title} ({'Created' if created else 'Exists'})")
except Exception as e:
    print(f"❌ Portfolio creation failed: {e}")

# Test 4: Create a company
try:
    client_user, created = User.objects.get_or_create(
        username='test_client',
        defaults={
            'email': 'client@test.com',
            'role': 'CLIENT'
        }
    )
    if created:
        client_user.set_password('testpass123')
        client_user.save()

    company, created = Company.objects.get_or_create(
        name='Tech Solutions Inc.',
        created_by=client_user,
        defaults={
            'description': 'A leading tech company',
            'contact_email': 'hr@techsolutions.com',
            'is_verified': True
        }
    )
    print(f"✅ Company: {company.name} ({'Created' if created else 'Exists'})")
except Exception as e:
    print(f"❌ Company creation failed: {e}")

# Test 5: Create a job posting
try:
    job, created = JobPosting.objects.get_or_create(
        title='Junior Django Developer',
        company=company,
        defaults={
            'description': 'We are looking for a Django developer...',
            'requirements': '2+ years experience with Django and Python',
            'job_type': 'FULL_TIME',
            'experience_level': 'JUNIOR',
            'salary_range': '$60,000 - $80,000',
            'location': 'Remote',
            'is_remote': True,
            'is_active': True
        }
    )

    # Add required skills
    python_skill, _ = Skill.objects.get_or_create(name='Python', defaults={'category': 'Programming'})
    django_skill, _ = Skill.objects.get_or_create(name='Django', defaults={'category': 'Web Development'})
    job.skills_required.add(python_skill, django_skill)

    print(f"✅ Job Posting: {job.title} at {job.company.name} ({'Created' if created else 'Exists'})")
    print(f"   Skills required: {[s.name for s in job.skills_required.all()]}")
except Exception as e:
    print(f"❌ Job posting creation failed: {e}")

print("\n📊 DATABASE SUMMARY")
print("===================")
print(f"Skills: {Skill.objects.count()}")
print(f"Users: {User.objects.count()}")
print(f"Portfolios: {Portfolio.objects.count()}")
print(f"Companies: {Company.objects.count()}")
print(f"Job Postings: {JobPosting.objects.count()}")
print(f"Applications: {Application.objects.count()}")

print("\n🎉 TALENT MODULE READY FOR DEVELOPMENT!")