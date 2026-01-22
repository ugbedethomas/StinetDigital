from rest_framework import serializers
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
