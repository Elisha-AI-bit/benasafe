from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.billing_dashboard, name='billing_dashboard'),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('payments/', views.payment_list, name='payment_list'),
    path('upgrade/', views.upgrade_plan, name='upgrade_plan'),
    path('payment/initiate/', views.initiate_payment, name='initiate_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
]
