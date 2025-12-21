from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Business

@login_required
def business_list(request):
    """List all businesses for the current user"""
    businesses = Business.objects.filter(user=request.user, is_active=True)
    return render(request, 'businesses/business_list.html', {'businesses': businesses})

@login_required
def business_create(request):
    """Create a new business"""
    if request.method == 'POST':
        messages.success(request, 'Business created successfully!')
        return redirect('businesses:business_list')
    return render(request, 'businesses/business_form.html')

@login_required
def business_detail(request, pk):
    """View business details"""
    business = get_object_or_404(Business, pk=pk, user=request.user)
    return render(request, 'businesses/business_detail.html', {'business': business})

@login_required
def business_update(request, pk):
    """Update business"""
    business = get_object_or_404(Business, pk=pk, user=request.user)
    if request.method == 'POST':
        messages.success(request, 'Business updated successfully!')
        return redirect('businesses:business_detail', pk=pk)
    return render(request, 'businesses/business_form.html', {'business': business})

@login_required
def business_delete(request, pk):
    """Delete business"""
    business = get_object_or_404(Business, pk=pk, user=request.user)
    business.is_active = False
    business.save()
    messages.success(request, 'Business deleted successfully!')
    return redirect('businesses:business_list')
