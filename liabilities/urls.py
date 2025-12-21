from django.urls import path
from . import views

app_name = 'liabilities'

urlpatterns = [
    path('', views.liability_list, name='liability_list'),
    path('add/', views.liability_create, name='liability_create'),
    path('<int:pk>/', views.liability_detail, name='liability_detail'),
    path('<int:pk>/edit/', views.liability_update, name='liability_update'),
    path('<int:pk>/delete/', views.liability_delete, name='liability_delete'),
    path('export/pdf/', views.export_liabilities_pdf, name='export_liabilities_pdf'),
    path('export/csv/', views.export_liabilities_csv, name='export_liabilities_csv'),
]
