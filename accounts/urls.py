from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('resend-verification/', views.resend_verification_email, name='resend_verification'),
    path('profile/', views.profile, name='profile'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/password-change-done/'
    ), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Admin URLs
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin/users/<int:user_id>/toggle-status/', views.admin_user_toggle_status, name='admin_user_toggle_status'),
    path('admin/bouquets/', views.admin_bouquet_management, name='admin_bouquet_management'),
    path('admin/verification-queue/', views.admin_verification_queue, name='admin_verification_queue'),
    path('admin/verify-user/<int:user_id>/', views.admin_verify_user, name='admin_verify_user'),
]
