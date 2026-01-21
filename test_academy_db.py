import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stinet_core.settings')
django.setup()

from academy.models import CourseCategory, Course, Module, Lesson, Enrollment
from users.models import User

print("🎓 Testing Academy Database Setup...")
print("=" * 50)

# Check tables exist
try:
    categories = CourseCategory.objects.count()
    courses = Course.objects.count()
    modules = Module.objects.count()
    lessons = Lesson.objects.count()
    enrollments = Enrollment.objects.count()

    print(f"✅ CourseCategory records: {categories}")
    print(f"✅ Course records: {courses}")
    print(f"✅ Module records: {modules}")
    print(f"✅ Lesson records: {lessons}")
    print(f"✅ Enrollment records: {enrollments}")

    # Create test data if empty
    if categories == 0:
        print("\n📝 Creating sample data...")

        # Create category
        web_dev = CourseCategory.objects.create(
            name="Web Development",
            description="Learn to build modern websites and web applications",
            icon="code",
            order=1
        )

        # Get or create instructor
        instructor, _ = User.objects.get_or_create(
            username="trainer.john",
            defaults={
                'email': 'john@stinet.digital',
                'role': 'TRAINER',
                'password': 'trainer123'
            }
        )

        # Create course
        python_course = Course.objects.create(
            title="Python & Django Full Stack",
            slug="python-django-full-stack",
            description="Complete course from Python basics to Django web development",
            category=web_dev,
            instructor=instructor,
            level="BEGINNER",
            price=50000.00,
            duration_hours=120,
            is_published=True
        )

        # Create modules
        module1 = Module.objects.create(
            course=python_course,
            title="Python Fundamentals",
            description="Learn Python basics",
            order=1
        )

        # Create lessons
        Lesson.objects.create(
            module=module1,
            title="Introduction to Python",
            content="Python is a versatile programming language...",
            video_url="https://example.com/video1",
            duration_minutes=15,
            order=1,
            is_free=True
        )

        print("✅ Sample data created successfully!")
        print(f"   Course: {python_course.title}")
        print(f"   Module: {module1.title}")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)