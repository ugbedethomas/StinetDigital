# create_sample_talent_data.py
import os
import django
import sys

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stinet_core.settings')
django.setup()

from talent.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


def create_sample_data():
    print("🔄 Creating sample talent data...")

    # Get existing users
    students = User.objects.filter(role='STUDENT')[:3]
    client = User.objects.filter(role='CLIENT').first()

    if not client:
        print("⚠️ No client user found. Creating one...")
        client = User.objects.create_user(
            username='sample_client',
            email='client@example.com',
            password='client123',
            role='CLIENT'
        )

    # Create skills
    skills_data = [
        ('Python', 'Programming'),
        ('Django', 'Web Development'),
        ('React', 'Frontend'),
        ('JavaScript', 'Programming'),
        ('PostgreSQL', 'Database'),
        ('AWS', 'Cloud'),
        ('Docker', 'DevOps'),
        ('Git', 'Tools'),
        ('HTML/CSS', 'Frontend'),
        ('REST API', 'Web Development'),
    ]

    skills = {}
    for name, category in skills_data:
        skill, _ = Skill.objects.get_or_create(
            name=name,
            defaults={'category': category, 'icon': 'code'}
        )
        skills[name] = skill
        print(f"✅ Skill: {name}")

    # Create company
    company, _ = Company.objects.get_or_create(
        name='Innovate Tech Solutions',
        created_by=client,
        defaults={
            'description': 'Leading technology solutions provider',
            'website': 'https://innovate-tech.com',
            'contact_email': 'careers@innovate-tech.com',
            'is_verified': True
        }
    )
    print(f"✅ Company: {company.name}")

    # Create job postings
    jobs_data = [
        {
            'title': 'Senior Django Developer',
            'description': 'Lead backend development for enterprise applications.',
            'requirements': '5+ years Django, Python expertise, PostgreSQL, REST APIs',
            'skills': ['Python', 'Django', 'PostgreSQL', 'REST API'],
            'type': 'FULL_TIME',
            'level': 'SENIOR',
            'salary': '$120,000 - $160,000',
            'location': 'San Francisco, CA',
            'remote': False
        },
        {
            'title': 'React Frontend Developer',
            'description': 'Build responsive user interfaces with React.',
            'requirements': '3+ years React, JavaScript, CSS, responsive design',
            'skills': ['React', 'JavaScript', 'HTML/CSS'],
            'type': 'REMOTE',
            'level': 'MID',
            'salary': '$90,000 - $120,000',
            'location': 'Remote',
            'remote': True
        },
        {
            'title': 'Full Stack Developer',
            'description': 'Work on both frontend and backend features.',
            'requirements': 'Python, Django, React, basic DevOps knowledge',
            'skills': ['Python', 'Django', 'React', 'JavaScript'],
            'type': 'FULL_TIME',
            'level': 'MID',
            'salary': '$100,000 - $130,000',
            'location': 'New York, NY',
            'remote': True
        },
        {
            'title': 'DevOps Engineer',
            'description': 'Manage cloud infrastructure and CI/CD pipelines.',
            'requirements': 'AWS, Docker, Kubernetes, CI/CD experience',
            'skills': ['AWS', 'Docker', 'Git'],
            'type': 'FULL_TIME',
            'level': 'SENIOR',
            'salary': '$130,000 - $170,000',
            'location': 'Remote',
            'remote': True
        },
    ]

    for job_data in jobs_data:
        job, created = JobPosting.objects.get_or_create(
            title=job_data['title'],
            company=company,
            defaults={
                'description': job_data['description'],
                'requirements': job_data['requirements'],
                'job_type': job_data['type'],
                'experience_level': job_data['level'],
                'salary_range': job_data['salary'],
                'location': job_data['location'],
                'is_remote': job_data['remote'],
                'is_active': True
            }
        )

        # Add required skills
        for skill_name in job_data['skills']:
            if skill_name in skills:
                job.skills_required.add(skills[skill_name])

        if created:
            print(f"✅ Job: {job.title}")

    # Create portfolios and skills for students
    for i, student in enumerate(students):
        # Create portfolio
        portfolio, _ = Portfolio.objects.get_or_create(
            student=student,
            defaults={
                'title': f"{student.username}'s Portfolio",
                'bio': f"Talented developer with expertise in multiple technologies. {['Passionate about clean code and user experience.', 'Experienced in building scalable applications.', 'Strong problem-solving skills.'][i % 3]}",
                'github_url': f'https://github.com/{student.username}',
                'linkedin_url': f'https://linkedin.com/in/{student.username}',
                'is_public': True
            }
        )

        # Add skills to students (different for each)
        student_skills = [
            ['Python', 'Django', 'PostgreSQL'],
            ['React', 'JavaScript', 'HTML/CSS'],
            ['Python', 'React', 'AWS', 'Docker']
        ][i % 3]

        for skill_name in student_skills:
            if skill_name in skills:
                StudentSkill.objects.get_or_create(
                    student=student,
                    skill=skills[skill_name],
                    defaults={
                        'proficiency': [2, 3, 4][i % 3],  # Varying proficiency
                        'verified': True
                    }
                )

        print(f"✅ Portfolio for: {student.username}")

    print("\n🎉 SAMPLE DATA CREATION COMPLETE!")
    print("\n📊 FINAL STATS:")
    print(f"   Skills: {Skill.objects.count()}")
    print(f"   Companies: {Company.objects.count()}")
    print(f"   Job Postings: {JobPosting.objects.count()}")
    print(f"   Active Jobs: {JobPosting.objects.filter(is_active=True).count()}")
    print(f"   Portfolios: {Portfolio.objects.count()}")
    print(f"   Student Skills: {StudentSkill.objects.count()}")

    print("\n🔗 TEST ENDPOINTS:")
    print("   GET /api/talent/api/jobs/")
    print("   GET /api/talent/api/skills/")
    print("   GET /api/talent/api/portfolios/")
    print("   GET /api/talent/jobs/recommended/ (when logged in as student)")


if __name__ == '__main__':
    create_sample_data()