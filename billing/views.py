from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def billing_dashboard(request):
    """Billing dashboard"""
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    return render(request, 'billing/dashboard.html')

@login_required
def subscription_list(request):
    """List all subscriptions"""
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    return render(request, 'billing/subscription_list.html')

@login_required
def payment_list(request):
    """List all payments"""
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    return render(request, 'billing/payment_list.html')

@login_required
def upgrade_plan(request):
    """Upgrade subscription plan"""
    return render(request, 'billing/upgrade.html')
