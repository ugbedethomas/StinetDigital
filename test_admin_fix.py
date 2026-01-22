import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stinet_core.settings')

try:
    django.setup()
    print("✅ Django setup successful")

    # Try to import admin
    from talent import admin

    print("✅ Talent admin imports successfully")

    # Check models
    from talent.models import Portfolio, Skill, Company

    print("✅ Talent models import successfully")

    print("\n🎉 Admin fix verified!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()