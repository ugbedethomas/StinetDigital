from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def talent_dashboard(request):
    return render(request, 'talent/dashboard.html')

def test_view(request):
    return JsonResponse({'status': 'Talent module working'})
