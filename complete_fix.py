# complete_fix.py
import os
import shutil

print("🔄 COMPLETE FIX FOR CORRUPTED FILES")
print("=====================================")

# Backup corrupted files
backup_dir = "backup_files"
os.makedirs(backup_dir, exist_ok=True)

files_to_fix = [
    'talent/urls.py',
    'talent/views.py',
    'talent/admin.py',
    'talent/models.py'
]

for filepath in files_to_fix:
    if os.path.exists(filepath):
        # Backup
        shutil.copy2(filepath, os.path.join(backup_dir, os.path.basename(filepath)))
        print(f"📁 Backed up: {filepath}")

        # Check for null bytes
        with open(filepath, 'rb') as f:
            content = f.read()
            if b'\x00' in content:
                print(f"  ❌ Contains null bytes - will recreate")

                # Recreate with clean content
                if filepath == 'talent/urls.py':
                    clean_content = b'''from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='talent_test'),
]
'''
                elif filepath == 'talent/views.py':
                    clean_content = b'''from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def talent_dashboard(request):
    return render(request, 'talent/dashboard.html')

def test_view(request):
    return JsonResponse({'status': 'Talent module working', 'message': 'API ready for development'})
'''
                elif filepath == 'talent/admin.py':
                    # Simple admin.py
                    clean_content = b'''from django.contrib import admin
from .models import Portfolio, Project, Skill, StudentSkill, Company, JobPosting, Application

# Register your models here
admin.site.register(Portfolio)
admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(StudentSkill)
admin.site.register(Company)
admin.site.register(JobPosting)
admin.site.register(Application)
'''
                elif filepath == 'talent/models.py':
                    # Keep existing models.py if it's not corrupted
                    # Just rewrite it to ensure no null bytes
                    clean_content = content.replace(b'\x00', b'')

                # Write clean file
                with open(filepath, 'wb') as f:
                    f.write(clean_content)
                print(f"  ✅ Recreated: {filepath}")
            else:
                print(f"  ✅ No null bytes found")

print("\n🎉 All files checked and fixed")

# Clear Python cache
print("\n🧹 Clearing Python cache...")
for root, dirs, files in os.walk('.'):
    for dir in dirs:
        if dir == '__pycache__':
            shutil.rmtree(os.path.join(root, dir), ignore_errors=True)
    for file in files:
        if file.endswith('.pyc'):
            os.remove(os.path.join(root, file))

print("\nNow testing Django...")