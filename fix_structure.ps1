# fix_structure.ps1
Write-Host "🔄 Fixing Django project structure..." -ForegroundColor Yellow

# 1. Check and fix stinet_core/urls.py
if (Test-Path stinet_core/urls.py) {
    # Backup the file
    Copy-Item stinet_core/urls.py stinet_core/urls.py.backup -Force
    Write-Host "📁 Backed up stinet_core/urls.py" -ForegroundColor Cyan
}

# Create clean urls.py
$urlsContent = @'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/academy/', include('academy.urls')),
    # Talent URLs will be added later
    # path('api/talent/', include('talent.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'@

$urlsContent | Out-File -FilePath "stinet_core/urls.py" -Encoding UTF8 -Force
Write-Host "✅ Created clean stinet_core/urls.py" -ForegroundColor Green

# 2. Create minimal talent/urls.py
$talentUrlsContent = @'
from django.urls import path

urlpatterns = [
    # Routes will be added when models are ready
]
'@

$talentUrlsContent | Out-File -FilePath "talent/urls.py" -Encoding UTF8 -Force
Write-Host "✅ Created minimal talent/urls.py" -ForegroundColor Green

# 3. Create minimal talent/views.py if it doesn't exist
if (-not (Test-Path talent/views.py)) {
    $viewsContent = @'
from django.http import HttpResponse

def index(request):
    return HttpResponse("Talent module - Coming soon")
'@
    $viewsContent | Out-File -FilePath "talent/views.py" -Encoding UTF8 -Force
    Write-Host "✅ Created talent/views.py" -ForegroundColor Green
}

# 4. Create empty talent/models.py if it doesn't exist
if (-not (Test-Path talent/models.py)) {
    "" | Out-File -FilePath "talent/models.py" -Encoding UTF8 -Force
    Write-Host "✅ Created empty talent/models.py" -ForegroundColor Green
}

# 5. Create empty talent/apps.py if it doesn't exist
if (-not (Test-Path talent/apps.py)) {
    $appsContent = @'
from django.apps import AppConfig

class TalentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'talent'
'@
    $appsContent | Out-File -FilePath "talent/apps.py" -Encoding UTF8 -Force
    Write-Host "✅ Created talent/apps.py" -ForegroundColor Green
}

Write-Host "`n📝 Checking Django setup..." -ForegroundColor Cyan