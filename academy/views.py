from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CourseCategory, Course, Module, Enrollment
from .serializers import (
    CourseCategorySerializer,
    CourseSerializer,
    SimpleCourseSerializer,
    ModuleSerializer,
    EnrollmentSerializer
)
from django.utils import timezone



class TestAcademyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            "message": "🎓 Academy API is working!",
            "endpoints": {
                "categories": "/api/academy/categories/",
                "courses": "/api/academy/courses/",
                "course_detail": "/api/academy/courses/<slug>/",
                "modules": "/api/academy/courses/<slug>/modules/",
                "enroll": "/api/academy/enroll/",
                "my_courses": "/api/academy/my-courses/",
                "dashboard": "/api/academy/dashboard/"
            }
        })


class CourseCategoryListView(generics.ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [permissions.AllowAny]


class CourseListView(generics.ListAPIView):
    serializer_class = SimpleCourseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Course.objects.filter(is_published=True)


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ModuleListView(generics.ListAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_slug = self.kwargs['slug']
        course = get_object_or_404(Course, slug=course_slug, is_published=True)
        return course.modules.all()


class EnrollmentCreateView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Only students can enroll
        if self.request.user.role != 'STUDENT':
            raise permissions.PermissionDenied("Only students can enroll in courses.")

        course = serializer.validated_data['course']

        # Check if already enrolled
        if Enrollment.objects.filter(student=self.request.user, course=course).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")

        serializer.save(student=self.request.user, status='ACTIVE')


class UserEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)


class StudentDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'STUDENT':
            return Response(
                {"error": "Only students can access dashboard"},
                status=status.HTTP_403_FORBIDDEN
            )

        enrollments = Enrollment.objects.filter(student=request.user)

        # Calculate statistics
        total_courses = enrollments.count()
        completed_courses = enrollments.filter(status='COMPLETED').count()
        active_courses = enrollments.filter(status='ACTIVE').count()

        data = {
            'student': {
                'username': request.user.username,
                'email': request.user.email,
                'role': request.user.role
            },
            'statistics': {
                'total_courses': total_courses,
                'completed_courses': completed_courses,
                'active_courses': active_courses,
                'completion_rate': (completed_courses / total_courses * 100) if total_courses > 0 else 0
            },
            'enrollments': EnrollmentSerializer(enrollments, many=True).data
        }

        return Response(data)

    from rest_framework import serializers  # Add this import if not present

    class EnrollmentCreateView(generics.CreateAPIView):
        """Enroll in a course"""
        serializer_class = EnrollmentSerializer
        permission_classes = [permissions.IsAuthenticated]

        def perform_create(self, serializer):
            # Only students can enroll
            if self.request.user.role != 'STUDENT':
                raise permissions.PermissionDenied("Only students can enroll in courses.")

            course = serializer.validated_data['course']

            # Check if already enrolled
            if Enrollment.objects.filter(student=self.request.user, course=course).exists():
                raise serializers.ValidationError("You are already enrolled in this course.")

            serializer.save(student=self.request.user, status='ACTIVE')

    class StudentDashboardView(APIView):
        """Student dashboard with enrolled courses and progress"""
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            if request.user.role != 'STUDENT':
                return Response(
                    {"error": "Only students can access dashboard"},
                    status=status.HTTP_403_FORBIDDEN
                )

            enrollments = Enrollment.objects.filter(student=request.user)

            # Calculate statistics
            total_courses = enrollments.count()
            completed_courses = enrollments.filter(status='COMPLETED').count()
            active_courses = enrollments.filter(status='ACTIVE').count()

            data = {
                'student': {
                    'username': request.user.username,
                    'email': request.user.email,
                    'role': request.user.role
                },
                'statistics': {
                    'total_courses': total_courses,
                    'completed_courses': completed_courses,
                    'active_courses': active_courses,
                    'completion_rate': (completed_courses / total_courses * 100) if total_courses > 0 else 0
                },
                'enrollments': EnrollmentSerializer(enrollments, many=True).data
            }

            return Response(data)

    class UpdateProgressView(APIView):
        """Update student progress in a course"""
        permission_classes = [permissions.IsAuthenticated]

        def post(self, request, enrollment_id):
            enrollment = get_object_or_404(
                Enrollment,
                id=enrollment_id,
                student=request.user
            )

            progress = request.data.get('progress')
            if progress is not None:
                try:
                    progress = int(progress)
                    if 0 <= progress <= 100:
                        enrollment.progress = progress
                        if progress == 100:
                            enrollment.status = 'COMPLETED'
                            enrollment.completed_at = timezone.now()
                        enrollment.save()

                        return Response({
                            "success": True,
                            "message": f"Progress updated to {progress}%",
                            "enrollment": EnrollmentSerializer(enrollment).data
                        })
                    else:
                        return Response(
                            {"error": "Progress must be between 0 and 100"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except ValueError:
                    return Response(
                        {"error": "Progress must be a number"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(
                {"error": "Progress value required"},
                status=status.HTTP_400_BAD_REQUEST
            )


from django.utils import timezone  # Add this import at top if not present
from rest_framework import serializers  # Add this import if not present


class UpdateProgressView(APIView):
    """Update student progress in a course"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, enrollment_id):
        enrollment = get_object_or_404(
            Enrollment,
            id=enrollment_id,
            student=request.user
        )

        progress = request.data.get('progress')
        if progress is not None:
            try:
                progress = int(progress)
                if 0 <= progress <= 100:
                    enrollment.progress = progress
                    if progress == 100:
                        enrollment.status = 'COMPLETED'
                        enrollment.completed_at = timezone.now()
                    enrollment.save()

                    return Response({
                        "success": True,
                        "message": f"Progress updated to {progress}%",
                        "enrollment": EnrollmentSerializer(enrollment).data
                    })
                else:
                    return Response(
                        {"error": "Progress must be between 0 and 100"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {"error": "Progress must be a number"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"error": "Progress value required"},
            status=status.HTTP_400_BAD_REQUEST
        )