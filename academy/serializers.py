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

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'category',
            'instructor', 'level', 'price', 'duration_hours', 'thumbnail',
            'is_published', 'created_at', 'updated_at'
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

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course',
            'enrolled_at', 'completed_at', 'status', 'progress'
        ]
        read_only_fields = ['enrolled_at', 'completed_at', 'status', 'progress']