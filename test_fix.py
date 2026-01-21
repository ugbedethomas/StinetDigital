import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stinet_core.settings')
django.setup()

print("🔧 Testing imports...")

try:
    from academy.views import (
        CourseDetailView, ModuleListView,
        EnrollmentCreateView, StudentDashboardView
    )
    print("✅ All views imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")

try:
    from academy.urls import urlpatterns
    print(f"✅ URLs configured: {len(urlpatterns)} patterns")
except Exception as e:
    print(f"❌ URLs error: {e}")

print("\n📁 Checking files exist:")
for file in ['academy/views.py', 'academy/urls.py', 'academy/serializers.py']:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} missing")