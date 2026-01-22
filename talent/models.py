from django.db import models
from django.conf import settings
from django.utils import timezone


class Portfolio(models.Model):
    """Student portfolio to showcase skills and projects"""
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolio',
        limit_choices_to={'role': 'STUDENT'}
    )
    title = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.student.username}'s Portfolio"


class Project(models.Model):
    """Project in a student's portfolio"""
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=500, help_text="Comma-separated list of technologies")
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='project_images/', blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-featured', '-created_at']

    def __str__(self):
        return self.title


class Skill(models.Model):
    """Skills that students can have"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=50, default='code')

    def __str__(self):
        return self.name


class StudentSkill(models.Model):
    """Bridge table for student skills with proficiency level"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.IntegerField(
        choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced'), (4, 'Expert')],
        default=1
    )
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_skills',
        limit_choices_to={'role__in': ['TRAINER', 'ADMIN', 'SUPER_ADMIN']}
    )

    class Meta:
        unique_together = ['student', 'skill']

    def __str__(self):
        return f"{self.student.username} - {self.skill.name} ({self.get_proficiency_display()})"


class Company(models.Model):
    """Companies that can post jobs and hire talent"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='companies',
        limit_choices_to={'role': 'CLIENT'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    """Job postings from companies"""

    class JobType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full Time'
        PART_TIME = 'PART_TIME', 'Part Time'
        CONTRACT = 'CONTRACT', 'Contract'
        INTERNSHIP = 'INTERNSHIP', 'Internship'
        REMOTE = 'REMOTE', 'Remote'

    class ExperienceLevel(models.TextChoices):
        ENTRY = 'ENTRY', 'Entry Level'
        JUNIOR = 'JUNIOR', 'Junior (1-3 years)'
        MID = 'MID', 'Mid Level (3-5 years)'
        SENIOR = 'SENIOR', 'Senior (5+ years)'
        LEAD = 'LEAD', 'Lead/Manager'

    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_postings')
    description = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JobType.choices)
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices)
    salary_range = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_remote = models.BooleanField(default=False)
    skills_required = models.ManyToManyField(Skill, related_name='job_postings')
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.title} at {self.company.name}"


class Application(models.Model):
    """Student applications for jobs"""

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        REVIEWED = 'REVIEWED', 'Reviewed'
        INTERVIEW = 'INTERVIEW', 'Interview Scheduled'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        WITHDRAWN = 'WITHDRAWN', 'Withdrawn'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'role': 'STUDENT'}
    )
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'job']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.username} → {self.job.title}"


class Interview(models.Model):
    """Interview scheduling"""
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='interview')
    scheduled_for = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    interview_type = models.CharField(
        max_length=50,
        choices=[
            ('PHONE', 'Phone Screen'),
            ('VIDEO', 'Video Call'),
            ('TECHNICAL', 'Technical Assessment'),
            ('ONSITE', 'On-site Interview')
        ]
    )
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"Interview for {self.application}"


class Placement(models.Model):
    """Successful placements (hired students)"""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='placements',
        limit_choices_to={'role': 'STUDENT'}
    )
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='placements')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='placements')
    start_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_current = models.BooleanField(default=True)
    placement_fee_paid = models.BooleanField(default=False)
    placement_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    placed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-placed_at']

    def __str__(self):
        return f"{self.student.username} placed at {self.company.name}"