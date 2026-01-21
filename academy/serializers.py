from rest_framework import serializers
from .models import CourseCategory, Course, Module, Lesson, Enrollment


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'description', 'icon', 'order']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'duration_minutes', 'order', 'is_free']


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'lessons']


class CourseSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer(read_only=True)
    instructor = serializers.StringRelatedField()
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'category',
            'instructor', 'level', 'price', 'duration_hours', 'thumbnail',
            'is_published', 'created_at', 'updated_at', 'modules'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SimpleCourseSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'category', 'level', 'price']


class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    course = SimpleCourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.filter(is_published=True),
        source='course',
        write_only=True
    )

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'course_id',
            'enrolled_at', 'completed_at', 'status', 'progress'
        ]
        read_only_fields = ['student', 'enrolled_at', 'completed_at', 'status', 'progress']