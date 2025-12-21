from django.urls import path
from . import views

app_name = 'professionals'

urlpatterns = [
    path('', views.professional_list, name='professional_list'),
    path('add/', views.professional_create, name='professional_create'),
    path('<int:pk>/', views.professional_detail, name='professional_detail'),
    path('<int:pk>/edit/', views.professional_update, name='professional_update'),
    path('<int:pk>/delete/', views.professional_delete, name='professional_delete'),
]
