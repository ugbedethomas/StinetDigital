# final_fix.ps1
Write-Host "🔧 FINAL FIX FOR STINET ERP PROJECT" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# 1. Fix the corrupted urls.py file
Write-Host "`n1. Fixing corrupted urls.py file..." -ForegroundColor Yellow

# Check what's currently in urls.py
try {
    $currentContent = Get-Content stinet_core/urls.py -Raw -ErrorAction Stop
    Write-Host "   Current file size: $($currentContent.Length) bytes" -ForegroundColor Gray
} catch {
    Write-Host "   Cannot read file (likely corrupted)" -ForegroundColor Red
}

# Create clean urls.py
$cleanUrls = @'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),  # Based on your backup
    path('api/academy/', include('academy.urls')),
    path('api/talent/', include('talent.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'@

# Write the file using binary mode to avoid encoding issues
$bytes = [System.Text.Encoding]::UTF8.GetBytes($cleanUrls)
[System.IO.File]::WriteAllBytes("$PWD\stinet_core\urls.py", $bytes)
Write-Host "   ✅ Created clean UTF-8 urls.py" -ForegroundColor Green

# 2. Create minimal talent/urls.py
Write-Host "`n2. Creating minimal talent/urls.py..." -ForegroundColor Yellow
$talentUrls = @'
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='talent_test'),
]
'@

$bytes = [System.Text.Encoding]::UTF8.GetBytes($talentUrls)
[System.IO.File]::WriteAllBytes("$PWD\talent\urls.py", $bytes)
Write-Host "   ✅ Created talent/urls.py" -ForegroundColor Green

# 3. Add test view to talent/views.py
Write-Host "`n3. Adding test view..." -ForegroundColor Yellow
$testView = @'

# Test view to verify module works
def test_view(request):
    from django.http import JsonResponse
    return JsonResponse({
        'status': 'success',
        'module': 'talent',
        'message': 'Talent pipeline module is working!',
        'endpoints_ready': False,
        'next_step': 'Run migrations and create models'
    })
'@

Add-Content -Path talent\views.py -Value $testView -Encoding UTF8
Write-Host "   ✅ Added test view" -ForegroundColor Green

# 4. Verify INSTALLED_APPS
Write-Host "`n4. Checking INSTALLED_APPS configuration..." -ForegroundColor Yellow
$settingsPath = "$PWD\stinet_core\settings.py"
$settingsContent = Get-Content $settingsPath -Raw

# Check for required apps
$requiredApps = @('users', 'academy', 'talent')
foreach ($app in $requiredApps) {
    if ($settingsContent -match "'$app'") {
        Write-Host "   ✅ '$app' found in INSTALLED_APPS" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  '$app' NOT found in INSTALLED_APPS" -ForegroundColor Yellow

        # Try to add it
        if ($app -eq 'talent') {
            # Add talent after academy
            if ($settingsContent -match "'academy',") {
                $settingsContent = $settingsContent -replace "'academy',", "'academy',`n    'talent',"
                $bytes = [System.Text.Encoding]::UTF8.GetBytes($settingsContent)
                [System.IO.File]::WriteAllBytes($settingsPath, $bytes)
                Write-Host "   ✅ Added 'talent' to INSTALLED_APPS" -ForegroundColor Green
            }
        }
    }
}

# 5. Test Django
Write-Host "`n5. Testing Django configuration..." -ForegroundColor Yellow
$output = python manage.py check 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Django check passed!" -ForegroundColor Green

    # 6. Run migrations
    Write-Host "`n6. Running migrations..." -ForegroundColor Yellow
    Write-Host "   Creating migrations for talent app..." -ForegroundColor Gray
    python manage.py makemigrations talent

    Write-Host "   Applying migrations..." -ForegroundColor Gray
    python manage.py migrate

    Write-Host "`n🎉 MIGRATIONS COMPLETE!" -ForegroundColor Green
    Write-Host "==========================" -ForegroundColor Green

    # 7. Test the server
    Write-Host "`n7. Testing the server..." -ForegroundColor Yellow
    Write-Host "   To start the server, run:" -ForegroundColor White
    Write-Host "   python manage.py runserver" -ForegroundColor Cyan
    Write-Host "`n   Then test these URLs:" -ForegroundColor White
    Write-Host "   - Admin: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
    Write-Host "   - Talent test: http://127.0.0.1:8000/api/talent/test/" -ForegroundColor Cyan
    Write-Host "   - Academy API: http://127.0.0.1:8000/api/academy/courses/" -ForegroundColor Cyan

} else {
    Write-Host "   ❌ Django check failed:" -ForegroundColor Red
    Write-Host $output -ForegroundColor Red
    Write-Host "`nPlease share the exact error message above." -ForegroundColor Yellow
}

Write-Host "`n🔍 DIAGNOSTIC INFORMATION:" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# Show file sizes to verify they're not corrupted
Write-Host "File sizes (should not be 0):" -ForegroundColor White
$files = @(
    "stinet_core/urls.py",
    "talent/urls.py",
    "talent/views.py",
    "talent/models.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        $status = if ($size -gt 0) { "✅" } else { "❌" }
        Write-Host "   $status $file : $size bytes" -ForegroundColor $(if ($size -gt 0) { "Green" } else { "Red" })
    } else {
        Write-Host "   ❌ $file : NOT FOUND" -ForegroundColor Red
    }
}