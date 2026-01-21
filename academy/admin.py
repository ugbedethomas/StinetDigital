from django.contrib import admin
from .models import CourseCategory, Course, Module, Lesson, Enrollment

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'icon']
    list_editable = ['order']
    search_fields = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'level', 'price', 'is_published']
    list_filter = ['category', 'level', 'is_published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    inlines = [LessonInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'status', 'progress']
    list_filter = ['status', 'course']
    search_fields = ['student__username', 'course__title']