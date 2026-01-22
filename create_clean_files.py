# create_clean_files.py
import os

print("🛠️ CREATING CLEAN FILES WITHOUT CORRUPTION")
print("==========================================")

# 1. Create clean talent/views.py
print("\n1. Creating clean talent/views.py...")
views_content = '''from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def talent_dashboard(request):
    """Talent dashboard view"""
    user = request.user
    context = {
        'user': user,
        'role': user.role,
        'is_student': user.role == 'STUDENT',
        'is_client': user.role == 'CLIENT',
        'is_admin': user.role in ['ADMIN', 'SUPER_ADMIN']
    }
    return render(request, 'talent/dashboard.html', context)

def test_view(request):
    """Test endpoint to verify module is working"""
    return JsonResponse({
        'status': 'success',
        'module': 'talent',
        'message': 'Talent Pipeline Module is operational!',
        'features': [
            'Portfolio Management',
            'Job Postings',
            'Job Matching Algorithm',
            'Applications System',
            'Company Portal',
            'Placement Tracking'
        ]
    })
'''

# Write in binary mode to avoid encoding issues
with open('talent/views.py', 'wb') as f:
    f.write(views_content.encode('utf-8'))
print("✅ Created clean talent/views.py")

# 2. Create clean talent/urls.py
print("\n2. Creating clean talent/urls.py...")
urls_content = '''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .simple_views import (
    PortfolioViewSet, SkillViewSet, CompanyViewSet,
    JobPostingViewSet, ApplicationViewSet
)

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'jobs', JobPostingViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('api/', include(router.urls)),
    path('test/', views.test_view, name='talent_test'),
    path('dashboard/', views.talent_dashboard, name='talent_dashboard'),
    path('jobs/recommended/', 
         JobPostingViewSet.as_view({'get': 'recommended'}), 
         name='recommended_jobs'),
]
'''

with open('talent/urls.py', 'wb') as f:
    f.write(urls_content.encode('utf-8'))
print("✅ Created clean talent/urls.py")

# 3. Create clean talent/serializers.py (simplified)
print("\n3. Creating clean talent/serializers.py...")
serializers_content = '''from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'icon']

class PortfolioSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'student', 'title', 'bio', 'github_url', 
                 'linkedin_url', 'website_url', 'is_public', 
                 'created_at', 'updated_at']

class CompanySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'website', 'logo', 
                 'contact_email', 'contact_phone', 'is_verified', 
                 'created_by', 'created_at']

class JobPostingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    skills_required = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'company', 'description', 
                 'requirements', 'job_type', 'experience_level', 
                 'salary_range', 'location', 'is_remote', 'skills_required',
                 'is_active', 'posted_at', 'deadline']

class ApplicationSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    job = JobPostingSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'student', 'job', 'cover_letter', 
                 'portfolio_url', 'resume', 'status', 'applied_at', 
                 'reviewed_at', 'notes']
'''

with open('talent/serializers.py', 'wb') as f:
    f.write(serializers_content.encode('utf-8'))
print("✅ Created clean talent/serializers.py")

# 4. Create clean stinet_core/urls.py
print("\n4. Creating clean stinet_core/urls.py...")
stinet_urls_content = '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/academy/', include('academy.urls')),
    path('api/talent/', include('talent.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

with open('stinet_core/urls.py', 'wb') as f:
    f.write(stinet_urls_content.encode('utf-8'))
print("✅ Created clean stinet_core/urls.py")

# 5. Check all files for null bytes
print("\n5. Verifying no null bytes...")
files = [
    'talent/views.py',
    'talent/urls.py',
    'talent/serializers.py',
    'stinet_core/urls.py'
]

all_clean = True
for filepath in files:
    with open(filepath, 'rb') as f:
        content = f.read()
        if b'\x00' in content:
            print(f"❌ {filepath} still has null bytes")
            all_clean = False
        else:
            print(f"✅ {filepath} is clean")

if all_clean:
    print("\n🎉 ALL FILES CLEAN AND READY!")
    print("\nNow run: python manage.py check")
else:
    print("\n⚠️  Some files still have issues")