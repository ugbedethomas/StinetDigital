from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import *

User = get_user_model()


class TalentModelsTest(TestCase):
    def setUp(self):
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

    def test_create_portfolio(self):
        portfolio = Portfolio.objects.create(
            student=self.student,
            title='My Portfolio',
            bio='Test bio'
        )
        self.assertEqual(str(portfolio), f"{self.student.username}'s Portfolio")

    def test_create_company(self):
        company = Company.objects.create(
            name='Test Company',
            created_by=self.client_user,
            contact_email='company@test.com'
        )
        self.assertEqual(str(company), 'Test Company')

    def test_create_job_posting(self):
        company = Company.objects.create(
            name='Test Company',
            created_by=self.client_user,
            contact_email='company@test.com'
        )

        job = JobPosting.objects.create(
            title='Test Job',
            company=company,
            description='Job description',
            requirements='Requirements',
            job_type='FULL_TIME',
            experience_level='JUNIOR'
        )
        self.assertEqual(str(job), 'Test Job at Test Company')


class TalentAPITest(APITestCase):
    def setUp(self):
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

        self.client.force_authenticate(user=self.student)

    def test_create_portfolio(self):
        url = '/api/talent/portfolios/'
        data = {
            'title': 'My Portfolio',
            'bio': 'Test bio',
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student']['username'], 'teststudent')

    def test_browse_jobs(self):
        # Create a company and job first
        company = Company.objects.create(
            name='Test Company',
            created_by=self.client_user,
            contact_email='company@test.com'
        )

        job = JobPosting.objects.create(
            title='Test Job',
            company=company,
            description='Job description',
            requirements='Requirements',
            job_type='FULL_TIME',
            experience_level='JUNIOR',
            is_active=True
        )

        url = '/api/talent/jobs/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_apply_for_job(self):
        # Create company and job
        company = Company.objects.create(
            name='Test Company',
            created_by=self.client_user,
            contact_email='company@test.com'
        )

        job = JobPosting.objects.create(
            title='Test Job',
            company=company,
            description='Job description',
            requirements='Requirements',
            job_type='FULL_TIME',
            experience_level='JUNIOR',
            is_active=True
        )

        url = '/api/talent/applications/'
        data = {
            'job_id': job.id,
            'cover_letter': 'I am interested in this position'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)