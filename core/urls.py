from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'core'

urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
