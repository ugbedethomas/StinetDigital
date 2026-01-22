# debug_error.py
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    # Try to import Django settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'stinet_core.settings'

    import django
    from django.conf import settings

    print("✅ Django imported successfully")
    print(f"Django version: {django.__version__}")

    # Try to access settings
    print(f"\nSettings:")
    print(
        f"  INSTALLED_APPS: {[app for app in settings.INSTALLED_APPS if 'talent' in app or 'users' in app or 'academy' in app]}")
    print(f"  ROOT_URLCONF: {settings.ROOT_URLCONF}")

    # Try to import the URL config
    print(f"\nTrying to import {settings.ROOT_URLCONF}...")
    module = __import__(settings.ROOT_URLCONF)
    print(f"✅ URL config imported: {module}")

except SyntaxError as e:
    print(f"\n❌ SYNTAX ERROR in file:")
    print(f"   Error: {e}")
    print(f"   File: {e.filename}")
    print(f"   Line: {e.lineno}")
    print(f"   Text: {e.text}")

    # Try to read the problematic file
    if hasattr(e, 'filename') and os.path.exists(e.filename):
        print(f"\n🔍 Checking file {e.filename}:")
        with open(e.filename, 'rb') as f:
            content = f.read()
            print(f"   Size: {len(content)} bytes")
            if b'\x00' in content:
                null_positions = [i for i, b in enumerate(content) if b == 0]
                print(f"   ❌ Contains null bytes at positions: {null_positions[:10]}")

                # Show context around null bytes
                for pos in null_positions[:3]:
                    start = max(0, pos - 20)
                    end = min(len(content), pos + 20)
                    context = content[start:end].decode('utf-8', errors='ignore')
                    print(f"\n   Context around byte {pos}:")
                    print(f"   {context}")
            else:
                print(f"   ✅ No null bytes found")

except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()