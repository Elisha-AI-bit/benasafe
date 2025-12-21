from django.urls import path
from . import views

app_name = 'verification'

urlpatterns = [
    path('', views.verification_dashboard, name='verification_dashboard'),
    path('pending/', views.pending_verifications, name='pending_verifications'),
    path('<int:pk>/', views.verification_detail, name='verification_detail'),
    path('<int:pk>/approve/', views.approve_verification, name='approve_verification'),
    path('<int:pk>/reject/', views.reject_verification, name='reject_verification'),
]
