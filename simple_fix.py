# simple_fix.py
import os

print("🔄 Fixing Django URLs configuration...")

# 1. Fix stinet_core/urls.py
print("1. Creating stinet_core/urls.py...")
urls_content = '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/academy/', include('academy.urls')),
    path('api/talent/', include('talent.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

with open('stinet_core/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)
print("   ✅ Created")

# 2. Check if talent is in INSTALLED_APPS
print("\n2. Checking INSTALLED_APPS...")
settings_path = 'stinet_core/settings.py'

with open(settings_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "'talent'" in content:
    print("   ✅ 'talent' already in INSTALLED_APPS")
else:
    # Add talent after academy
    if "'academy'," in content:
        content = content.replace("'academy',", "'academy',\n    'talent',")
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   ✅ Added 'talent' to INSTALLED_APPS")
    else:
        print("   ⚠️  Could not find 'academy' in INSTALLED_APPS")

# 3. Create simple talent/urls.py
print("\n3. Creating talent/urls.py...")
talent_urls = '''from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='talent_test'),
]
'''

with open('talent/urls.py', 'w', encoding='utf-8') as f:
    f.write(talent_urls)
print("   ✅ Created")

print("\n🎉 Fixes applied successfully!")
print("\nNow run: python manage.py check")