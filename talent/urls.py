from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='talent_test'),
    path('dashboard/', views.talent_dashboard, name='talent_dashboard'),
]
