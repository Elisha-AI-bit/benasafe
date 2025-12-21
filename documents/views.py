from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.conf import settings

from .models import Document

@login_required
def document_list(request):
    """List all documents for the current user"""
    documents = Document.objects.filter(user=request.user)
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_upload(request):
    """Upload a new document"""
    if request.method == 'POST':
        messages.success(request, 'Document uploaded successfully!')
        return redirect('documents:document_list')
    return render(request, 'documents/document_upload.html')

@login_required
def document_detail(request, pk):
    """View document details"""
    document = get_object_or_404(Document, pk=pk, user=request.user)
    return render(request, 'documents/document_detail.html', {'document': document})

@login_required
def document_download(request, pk):
    """Download document"""
    document = get_object_or_404(Document, pk=pk, user=request.user)
    try:
        response = HttpResponse(document.file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
        return response
    except FileNotFoundError:
        raise Http404("Document not found")

@login_required
def document_delete(request, pk):
    """Delete document"""
    document = get_object_or_404(Document, pk=pk, user=request.user)
    document.delete()
    messages.success(request, 'Document deleted successfully!')
    return redirect('documents:document_list')

@login_required
def bulk_download(request):
    """Bulk download documents"""
    return render(request, 'documents/bulk_download.html')
