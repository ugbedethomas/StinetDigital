# fix_simplejwt.py
import subprocess
import sys

print("🔧 Fixing rest_framework_simplejwt dependency issue...")

# Install setuptools
print("\n1. Installing setuptools...")
result = subprocess.run([sys.executable, "-m", "pip", "install", "setuptools"],
                        capture_output=True, text=True)
if result.returncode == 0:
    print("✅ setuptools installed/updated")
else:
    print("❌ Failed to install setuptools:")
    print(result.stderr)

# Check simplejwt
print("\n2. Checking djangorestframework-simplejwt...")
try:
    import pkg_resources

    print("✅ pkg_resources is available")
except ImportError:
    print("❌ pkg_resources not available")
    print("   This should have been fixed by installing setuptools")

try:
    import rest_framework_simplejwt

    print("✅ rest_framework_simplejwt imports successfully")
    print(f"   Version: {rest_framework_simplejwt.__version__}")
except ImportError as e:
    print(f"❌ rest_framework_simplejwt import failed: {e}")

# Test Django
print("\n3. Testing Django setup...")
result = subprocess.run([sys.executable, "manage.py", "check"],
                        capture_output=True, text=True)
if result.returncode == 0:
    print("✅ Django check passed!")
    print("\n🚀 Ready to start server:")
    print("python manage.py runserver 8001")
else:
    print("❌ Django check failed:")
    print(result.stderr[:500])  # Show first 500 chars of error

    # Try alternative test
    print("\n🔍 Trying alternative import test...")
    test_code = '''
import os
import sys
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stinet_core.settings")
try:
    import django
    django.setup()
    print("SUCCESS: Django setup")

    # Check each app
    from django.apps import apps
    for app in ["users", "academy", "talent"]:
        try:
            apps.get_app_config(app)
            print(f"  ✅ {app} app registered")
        except:
            print(f"  ❌ {app} app not found")

except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
    '''

    result = subprocess.run([sys.executable, "-c", test_code],
                            capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr[:500])