from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import *

User = get_user_model()


class TalentAPITests(APITestCase):
    def setUp(self):
        # Create test users
        self.student = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123',
            role='STUDENT'
        )
        self.client_user = User.objects.create_user(
            username='testclient',
            email='client@test.com',
            password='testpass123',
            role='CLIENT'
        )
        self.admin = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123',
            role='ADMIN'
        )

        # Create skill
        self.skill = Skill.objects.create(
            name='Python',
            category='Programming',
            icon='code'
        )

        # Create company
        self.company = Company.objects.create(
            name='Test Company',
            created_by=self.client_user,
            contact_email='company@test.com',
            is_verified=True
        )

        # Create job posting
        self.job = JobPosting.objects.create(
            title='Test Developer',
            company=self.company,
            description='Test job description',
            requirements='Test requirements',
            job_type='FULL_TIME',
            experience_level='JUNIOR',
            is_active=True
        )
        self.job.skills_required.add(self.skill)

        # Create portfolio for student
        self.portfolio = Portfolio.objects.create(
            student=self.student,
            title='Test Portfolio',
            bio='Test bio'
        )

    def test_talent_test_endpoint(self):
        """Test the basic test endpoint"""
        url = '/api/talent/test/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Talent Pipeline Module', response.data['message'])

    def test_get_jobs(self):
        """Test getting job listings"""
        url = '/api/talent/api/jobs/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_skills(self):
        """Test getting skills list"""
        url = '/api/talent/api/skills/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_student_can_create_portfolio(self):
        """Test student can create portfolio"""
        self.client.force_authenticate(user=self.student)
        url = '/api/talent/api/portfolios/'
        data = {
            'title': 'My New Portfolio',
            'bio': 'This is my portfolio',
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student']['username'], 'teststudent')

    def test_client_can_create_company(self):
        """Test client can create company"""
        self.client.force_authenticate(user=self.client_user)
        url = '/api/talent/api/companies/'
        data = {
            'name': 'New Tech Company',
            'description': 'A new tech company',
            'contact_email': 'info@newtech.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Tech Company')

    def test_student_can_apply_for_job(self):
        """Test student can apply for a job"""
        self.client.force_authenticate(user=self.student)
        url = '/api/talent/api/applications/'
        data = {
            'job_id': self.job.id,
            'cover_letter': 'I am interested in this position'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['job']['title'], 'Test Developer')

    def test_recommended_jobs_endpoint(self):
        """Test recommended jobs for student"""
        # Add skill to student
        StudentSkill.objects.create(
            student=self.student,
            skill=self.skill,
            proficiency=3,
            verified=True
        )

        self.client.force_authenticate(user=self.student)
        url = '/api/talent/jobs/recommended/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Student should have at least 1 recommended job (100% match)
        self.assertGreaterEqual(len(response.data), 1)