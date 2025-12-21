from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Professional

@login_required
def professional_list(request):
    """List all professionals for the current user"""
    professionals = Professional.objects.filter(user=request.user, is_active=True)
    return render(request, 'professionals/professional_list.html', {'professionals': professionals})

@login_required
def professional_create(request):
    """Create a new professional"""
    if request.method == 'POST':
        messages.success(request, 'Professional added successfully!')
        return redirect('professionals:professional_list')
    return render(request, 'professionals/professional_form.html')

@login_required
def professional_detail(request, pk):
    """View professional details"""
    professional = get_object_or_404(Professional, pk=pk, user=request.user)
    return render(request, 'professionals/professional_detail.html', {'professional': professional})

@login_required
def professional_update(request, pk):
    """Update professional"""
    professional = get_object_or_404(Professional, pk=pk, user=request.user)
    if request.method == 'POST':
        messages.success(request, 'Professional updated successfully!')
        return redirect('professionals:professional_detail', pk=pk)
    return render(request, 'professionals/professional_form.html', {'professional': professional})

@login_required
def professional_delete(request, pk):
    """Delete professional"""
    professional = get_object_or_404(Professional, pk=pk, user=request.user)
    professional.is_active = False
    professional.save()
    messages.success(request, 'Professional deleted successfully!')
    return redirect('professionals:professional_list')
