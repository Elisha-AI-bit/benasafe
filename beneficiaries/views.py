from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import io

from .models import Beneficiary

@login_required
def beneficiary_list(request):
    """List all beneficiaries for the current user"""
    beneficiaries = Beneficiary.objects.filter(user=request.user, is_active=True)
    return render(request, 'beneficiaries/beneficiary_list.html', {'beneficiaries': beneficiaries})

@login_required
def beneficiary_create(request):
    """Create a new beneficiary"""
    if request.method == 'POST':
        messages.success(request, 'Beneficiary added successfully!')
        return redirect('beneficiaries:beneficiary_list')
    return render(request, 'beneficiaries/beneficiary_form.html')

@login_required
def beneficiary_detail(request, pk):
    """View beneficiary details"""
    beneficiary = get_object_or_404(Beneficiary, pk=pk, user=request.user)
    return render(request, 'beneficiaries/beneficiary_detail.html', {'beneficiary': beneficiary})

@login_required
def beneficiary_update(request, pk):
    """Update beneficiary"""
    beneficiary = get_object_or_404(Beneficiary, pk=pk, user=request.user)
    if request.method == 'POST':
        messages.success(request, 'Beneficiary updated successfully!')
        return redirect('beneficiaries:beneficiary_detail', pk=pk)
    return render(request, 'beneficiaries/beneficiary_form.html', {'beneficiary': beneficiary})

@login_required
def beneficiary_delete(request, pk):
    """Delete beneficiary"""
    beneficiary = get_object_or_404(Beneficiary, pk=pk, user=request.user)
    beneficiary.is_active = False
    beneficiary.save()
    messages.success(request, 'Beneficiary deleted successfully!')
    return redirect('beneficiaries:beneficiary_list')

@login_required
def export_beneficiaries_pdf(request):
    """Export all beneficiaries as PDF"""
    beneficiaries = Beneficiary.objects.filter(user=request.user, is_active=True)

    # Create PDF buffer
    buffer = io.BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph("BeneSafe - Beneficiaries Report", styles['Heading1'])
    story.append(title)
    story.append(Spacer(1, 12))

    # User info
    user_info = Paragraph(f"Generated for: {request.user.get_full_name()} ({request.user.username})", styles['Normal'])
    story.append(user_info)
    story.append(Spacer(1, 12))

    # Beneficiaries data
    if beneficiaries:
        data = [['Name', 'Relationship', 'Phone', 'Email', 'Address']]

        for beneficiary in beneficiaries:
            data.append([
                beneficiary.name,
                beneficiary.get_relationship_display(),
                beneficiary.phone,
                beneficiary.email or '',
                beneficiary.address or ''
            ])

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(table)
    else:
        no_data = Paragraph("No beneficiaries found.", styles['Normal'])
        story.append(no_data)

    # Build PDF
    doc.build(story)

    # Return PDF response
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="beneficiaries_{request.user.username}.pdf"'
    return response
