# final_compatibility_fix.py
import os
import subprocess
import sys

print("🎯 FINAL COMPATIBILITY FIX FOR STINET ERP")
print("=========================================")

# 1. Remove django-filter
print("\n1. Removing incompatible django-filter...")
try:
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "django-filter", "-y"],
                   check=True, capture_output=True, text=True)
    print("   ✅ django-filter uninstalled")
except:
    print("   ⚠️ Could not uninstall django-filter (may not be installed)")

# 2. Fix all necessary files
print("\n2. Fixing Django files...")

# Fix talent/views.py
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
        ],
        'next_steps': 'Create API endpoints and frontend interface'
    })
'''

with open('talent/views.py', 'w', encoding='utf-8') as f:
    f.write(views_content)
print("   ✅ Fixed talent/views.py")

# Fix talent/simple_views.py
simple_views_content = '''# talent/simple_views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *

User = get_user_model()

class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            return Portfolio.objects.filter(student=user)
        elif user.role in ['ADMIN', 'SUPER_ADMIN']:
            return Portfolio.objects.all()
        else:
            return Portfolio.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return Company.objects.filter(created_by=user)
        elif user.role in ['ADMIN', 'SUPER_ADMIN']:
            return Company.objects.all()
        return Company.objects.filter(is_verified=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class JobPostingViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = JobPosting.objects.filter(is_active=True)

        # Manual filtering without django-filter
        job_type = self.request.query_params.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)

        experience_level = self.request.query_params.get('experience_level')
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)

        is_remote = self.request.query_params.get('is_remote')
        if is_remote:
            queryset = queryset.filter(is_remote=is_remote.lower() == 'true')

        return queryset

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get jobs recommended for the current student"""
        if request.user.role != 'STUDENT':
            return Response(
                {'error': 'Only students can get recommended jobs'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        jobs = JobPosting.objects.filter(is_active=True)
        job_data = []

        for job in jobs:
            # Get student skills
            student_skills = set(
                request.user.skills.filter(verified=True).values_list('skill__name', flat=True)
            )
            job_skills = set(job.skills_required.values_list('name', flat=True))

            if job_skills:
                match_score = len(student_skills.intersection(job_skills)) / len(job_skills) * 100
                if match_score >= 30:
                    serializer = self.get_serializer(job)
                    job_data.append({
                        'job': serializer.data,
                        'match_score': round(match_score, 1)
                    })

        job_data.sort(key=lambda x: x['match_score'], reverse=True)
        return Response(job_data)

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'STUDENT':
            return Application.objects.filter(student=user)
        elif user.role == 'CLIENT':
            companies = Company.objects.filter(created_by=user)
            return Application.objects.filter(job__company__in=companies)
        elif user.role in ['ADMIN', 'SUPER_ADMIN']:
            return Application.objects.all()
        return Application.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
'''

with open('talent/simple_views.py', 'w', encoding='utf-8') as f:
    f.write(simple_views_content)
print("   ✅ Created talent/simple_views.py")

# Fix talent/urls.py
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

with open('talent/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)
print("   ✅ Fixed talent/urls.py")

# 3. Remove any api_views.py file that might have django-filter imports
api_views_path = 'talent/api_views.py'
if os.path.exists(api_views_path):
    os.remove(api_views_path)
    print("   ✅ Removed talent/api_views.py (had django-filter imports)")

# 4. Check settings.py for django-filter references
print("\n3. Checking settings.py...")
settings_path = 'stinet_core/settings.py'
if os.path.exists(settings_path):
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove django_filters from INSTALLED_APPS
    if "'django_filters'" in content:
        content = content.replace("'django_filters',", "")
        content = content.replace("'django_filters'", "")

    # Remove DjangoFilterBackend from REST_FRAMEWORK
    if 'DjangoFilterBackend' in content:
        content = content.replace("'django_filters.rest_framework.DjangoFilterBackend',", "")

    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("   ✅ Cleaned settings.py")

print("\n🎉 ALL FIXES APPLIED SUCCESSFULLY!")
print("\n🔧 Now testing Django...")

# Test Django
try:
    result = subprocess.run([sys.executable, "manage.py", "check"],
                            capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Django check PASSED!")
        print("\n🚀 Server ready to start!")
        print("Run: python manage.py runserver 8001")
        print("\n🔗 Test endpoints:")
        print("   http://127.0.0.1:8001/api/talent/test/")
        print("   http://127.0.0.1:8001/api/talent/api/jobs/")
        print("   http://127.0.0.1:8001/admin/")
    else:
        print("❌ Django check FAILED:")
        print(result.stderr)
except Exception as e:
    print(f"❌ Error testing Django: {e}")