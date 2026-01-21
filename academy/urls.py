from django.urls import path
from .views import (
    CourseCategoryListView,
    CourseListView,
    CourseDetailView,
    TestAcademyView,
    UserEnrollmentsView,
    EnrollmentCreateView,
    StudentDashboardView,
    UpdateProgressView  # ADD THIS
)

urlpatterns = [
    # Public endpoints
    path('test/', TestAcademyView.as_view(), name='test'),
    path('categories/', CourseCategoryListView.as_view(), name='categories'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),

    # Protected endpoints (require authentication)
    path('enroll/', EnrollmentCreateView.as_view(), name='enroll'),
    path('my-courses/', UserEnrollmentsView.as_view(), name='my_courses'),
    path('dashboard/', StudentDashboardView.as_view(), name='dashboard'),
    path('enrollments/<int:enrollment_id>/progress/', UpdateProgressView.as_view(), name='update_progress'),
    # ADD THIS BACK
]