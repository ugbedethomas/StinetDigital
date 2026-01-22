from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import (
    Portfolio, Project, Skill, StudentSkill,
    Company, JobPosting, Application, Interview, Placement
)

User = get_user_model()

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('student__username', 'student__email', 'title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'portfolio', 'featured', 'created_at')
    list_filter = ('featured', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    raw_id_fields = ('portfolio',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon')
    list_filter = ('category',)
    search_fields = ('name', 'category')

@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill', 'proficiency', 'verified')
    list_filter = ('verified', 'proficiency', 'skill__category')
    search_fields = ('student__username', 'skill__name')
    raw_id_fields = ('student', 'skill', 'verified_by')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_verified', 'contact_email', 'created_by')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('name', 'description', 'contact_email')
    raw_id_fields = ('created_by',)

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'experience_level', 'is_active', 'posted_at')
    list_filter = ('is_active', 'job_type', 'experience_level', 'posted_at')
    search_fields = ('title', 'description', 'company__name')
    filter_horizontal = ('skills_required',)
    raw_id_fields = ('company',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'status', 'applied_at', 'reviewed_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('student__username', 'job__title', 'cover_letter')
    raw_id_fields = ('student', 'job')
    readonly_fields = ('applied_at',)

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'scheduled_for', 'interview_type', 'completed')
    list_filter = ('completed', 'interview_type', 'scheduled_for')
    search_fields = ('application__student__username', 'application__job__title')
    raw_id_fields = ('application',)

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'job', 'start_date', 'is_current')
    list_filter = ('is_current', 'placement_fee_paid', 'placed_at')
    search_fields = ('student__username', 'company__name', 'job__title')
    raw_id_fields = ('student', 'job', 'company')