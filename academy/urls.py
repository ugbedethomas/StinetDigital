from django.urls import path
from .views import CourseCategoryListView, CourseListView, TestAcademyView, UserEnrollmentsView

urlpatterns = [
    path('test/', TestAcademyView.as_view(), name='test'),
    path('categories/', CourseCategoryListView.as_view(), name='categories'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('my-courses/', UserEnrollmentsView.as_view(), name='my_courses'),
]