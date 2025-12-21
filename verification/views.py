from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Verification

@login_required
def verification_dashboard(request):
    """Verification dashboard"""
    if request.user.userprofile.role not in ['verifier', 'admin']:
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    verifications = Verification.objects.all()
    return render(request, 'verification/dashboard.html', {'verifications': verifications})

@login_required
def pending_verifications(request):
    """List pending verifications"""
    if request.user.userprofile.role not in ['verifier', 'admin']:
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    verifications = Verification.objects.filter(status='pending')
    return render(request, 'verification/pending.html', {'verifications': verifications})

@login_required
def verification_detail(request, pk):
    """View verification details"""
    verification = get_object_or_404(Verification, pk=pk)
    if request.user.userprofile.role not in ['verifier', 'admin'] and request.user != verification.user:
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    return render(request, 'verification/detail.html', {'verification': verification})

@login_required
def approve_verification(request, pk):
    """Approve verification"""
    verification = get_object_or_404(Verification, pk=pk)
    if request.user.userprofile.role not in ['verifier', 'admin']:
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    verification.status = 'approved'
    verification.verifier = request.user
    verification.save()
    messages.success(request, 'Verification approved successfully!')
    return redirect('verification:verification_detail', pk=pk)

@login_required
def reject_verification(request, pk):
    """Reject verification"""
    verification = get_object_or_404(Verification, pk=pk)
    if request.user.userprofile.role not in ['verifier', 'admin']:
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    verification.status = 'rejected'
    verification.verifier = request.user
    verification.save()
    messages.success(request, 'Verification rejected')
    return redirect('verification:verification_detail', pk=pk)
