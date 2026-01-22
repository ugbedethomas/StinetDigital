# remove_django_filters.py
import os
import re

print("🔧 Removing django_filters from settings.py...")

settings_path = "stinet_core/settings.py"

if os.path.exists(settings_path):
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if django_filters is in INSTALLED_APPS
    if "'django_filters'" in content or '"django_filters"' in content:
        print("❌ Found 'django_filters' in settings.py")

        # Remove from INSTALLED_APPS
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            # Remove lines containing django_filters
            if "'django_filters'" in line or '"django_filters"' in line:
                print(f"   Removing: {line.strip()}")
                continue
            new_lines.append(line)

        new_content = '\n'.join(new_lines)

        # Also remove from REST_FRAMEWORK if present
        new_content = new_content.replace(
            "'django_filters.rest_framework.DjangoFilterBackend',",
            ""
        )
        new_content = new_content.replace(
            '"django_filters.rest_framework.DjangoFilterBackend",',
            ""
        )

        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("✅ Removed django_filters from settings.py")
    else:
        print("✅ django_filters not found in settings.py")

    # Check for any other references
    if 'django_filters' in content.lower():
        print("⚠️  Warning: Other references to django_filters found")
        # Show them
        for i, line in enumerate(content.split('\n'), 1):
            if 'django_filters' in line.lower():
                print(f"   Line {i}: {line.strip()}")
else:
    print("❌ settings.py not found")

print("\n🔍 Now testing Django...")
import subprocess

result = subprocess.run(["python", "manage.py", "check"],
                        capture_output=True, text=True)
if result.returncode == 0:
    print("✅ Django check passed!")
    print("\n🚀 Ready to start server:")
    print("python manage.py runserver 8001")
else:
    print("❌ Django check failed:")
    print(result.stderr)