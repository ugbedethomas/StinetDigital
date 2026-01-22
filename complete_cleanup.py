# complete_cleanup.py
import os
import re

print("🧹 COMPLETE CLEANUP - Removing all django_filters references")
print("==========================================================")

# Files to check and clean
files_to_check = [
    'stinet_core/settings.py',
    'talent/views.py',
    'talent/simple_views.py',
    'talent/api_views.py' if os.path.exists('talent/api_views.py') else None,
    'talent/serializers.py',
    'talent/urls.py',
]

# Remove None values
files_to_check = [f for f in files_to_check if f]

for filepath in files_to_check:
    if os.path.exists(filepath):
        print(f"\n🔍 Checking {filepath}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for django_filters references
        if 'django_filters' in content.lower():
            print(f"   ❌ Found django_filters references")

            # Remove import lines
            lines = content.split('\n')
            new_lines = []
            removed_count = 0

            for line in lines:
                if 'django_filters' in line.lower():
                    print(f"      Removing: {line.strip()[:50]}...")
                    removed_count += 1
                    continue
                new_lines.append(line)

            if removed_count > 0:
                new_content = '\n'.join(new_lines)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"   ✅ Removed {removed_count} references")
            else:
                print("   ⚠️  Found reference but couldn't remove")
        else:
            print("   ✅ No django_filters references found")

# Also check for any .pyc files or __pycache__
print("\n🧹 Cleaning Python cache...")
for root, dirs, files in os.walk('.'):
    # Remove __pycache__ directories
    for dir_name in dirs:
        if dir_name == '__pycache__':
            cache_dir = os.path.join(root, dir_name)
            try:
                import shutil

                shutil.rmtree(cache_dir)
                print(f"   Removed: {cache_dir}")
            except:
                pass

    # Remove .pyc files
    for file_name in files:
        if file_name.endswith('.pyc'):
            pyc_file = os.path.join(root, file_name)
            try:
                os.remove(pyc_file)
                print(f"   Removed: {pyc_file}")
            except:
                pass

print("\n🎉 Cleanup complete!")
print("\n🔍 Now testing Django...")

import subprocess

result = subprocess.run(["python", "manage.py", "check"],
                        capture_output=True, text=True)
if result.returncode == 0:
    print("✅ Django check passed!")
    print("\n🎯 You can now:")
    print("   1. Run server: python manage.py runserver 8001")
    print("   2. Test endpoints")
else:
    print("❌ Django check failed:")
    print(result.stderr)
    print("\n💡 Try running: python manage.py check --traceback")