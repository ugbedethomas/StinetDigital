from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CourseCategory, Course, Enrollment
from .serializers import CourseCategorySerializer, SimpleCourseSerializer, EnrollmentSerializer


class CourseCategoryListView(generics.ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [permissions.AllowAny]


class CourseListView(generics.ListAPIView):
    serializer_class = SimpleCourseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Course.objects.filter(is_published=True)


class TestAcademyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "message": "🎓 Academy API is working!",
            "endpoints": {
                "categories": "/api/academy/categories/",
                "courses": "/api/academy/courses/",
                "my-courses": "/api/academy/my-courses/"
            }
        })


class UserEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)