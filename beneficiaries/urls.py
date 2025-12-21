from django.urls import path
from . import views

app_name = 'beneficiaries'

urlpatterns = [
    path('', views.beneficiary_list, name='beneficiary_list'),
    path('add/', views.beneficiary_create, name='beneficiary_create'),
    path('<int:pk>/', views.beneficiary_detail, name='beneficiary_detail'),
    path('<int:pk>/edit/', views.beneficiary_update, name='beneficiary_update'),
    path('<int:pk>/delete/', views.beneficiary_delete, name='beneficiary_delete'),
    path('export/pdf/', views.export_beneficiaries_pdf, name='export_beneficiaries_pdf'),
]
