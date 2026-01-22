from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def talent_dashboard(request):
    """Talent dashboard view"""
    user = request.user
    context = {
        'user': user,
        'role': user.role,
        'is_student': user.role == 'STUDENT',
        'is_client': user.role == 'CLIENT',
        'is_admin': user.role in ['ADMIN', 'SUPER_ADMIN']
    }
    return render(request, 'talent/dashboard.html', context)

def test_view(request):
    """Test endpoint to verify module is working"""
    return JsonResponse({
        'status': 'success',
        'module': 'talent',
        'message': 'Talent Pipeline Module is operational!',
        'features': [
            'Portfolio Management',
            'Job Postings',
            'Job Matching Algorithm',
            'Applications System',
            'Company Portal',
            'Placement Tracking'
        ]
    })
