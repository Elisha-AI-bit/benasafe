from django.urls import path
from . import views

app_name = 'businesses'

urlpatterns = [
    path('', views.business_list, name='business_list'),
    path('add/', views.business_create, name='business_create'),
    path('<int:pk>/', views.business_detail, name='business_detail'),
    path('<int:pk>/edit/', views.business_update, name='business_update'),
    path('<int:pk>/delete/', views.business_delete, name='business_delete'),
]
