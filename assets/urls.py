from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    
    # Bank Account URLs
    path('bank-accounts/', views.bank_account_list, name='bank_account_list'),
    path('bank-accounts/add/', views.bank_account_create, name='bank_account_create'),
    path('bank-accounts/<int:pk>/', views.bank_account_detail, name='bank_account_detail'),
    path('bank-accounts/<int:pk>/edit/', views.bank_account_update, name='bank_account_update'),
    path('bank-accounts/<int:pk>/delete/', views.bank_account_delete, name='bank_account_delete'),

    # Insurance URLs
    path('insurance/', views.insurance_list, name='insurance_list'),
    path('insurance/add/', views.insurance_create, name='insurance_create'),
    path('insurance/<int:pk>/', views.insurance_detail, name='insurance_detail'),
    path('insurance/<int:pk>/edit/', views.insurance_update, name='insurance_update'),
    path('insurance/<int:pk>/delete/', views.insurance_delete, name='insurance_delete'),

    # Motor Vehicle URLs
    path('vehicles/', views.motor_vehicle_list, name='motor_vehicle_list'),
    path('vehicles/add/', views.motor_vehicle_create, name='motor_vehicle_create'),

    # House and Land URLs
    path('properties/', views.house_land_list, name='house_land_list'),
    path('properties/add/', views.house_land_create, name='house_land_create'),

    # Project URLs
    path('projects/', views.project_list, name='project_list'),
    path('projects/add/', views.project_create, name='project_create'),

    # Document URLs
    path('<int:pk>/documents/', views.asset_documents, name='asset_documents'),
    path('<int:pk>/documents/add/', views.asset_document_upload, name='asset_document_upload'),
    path('documents/<int:pk>/delete/', views.asset_document_delete, name='asset_document_delete'),

    # Export URLs
    path('export/pdf/', views.export_assets_pdf, name='export_assets_pdf'),
    path('export/csv/', views.export_assets_csv, name='export_assets_csv'),
]
