# talent/simple_views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
        return JobPosting.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        if request.user.role != 'STUDENT':
            return Response({'error': 'Only students can get recommended jobs'}, status=400)
        
        jobs = JobPosting.objects.filter(is_active=True)
        job_data = []
        
        for job in jobs:
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
