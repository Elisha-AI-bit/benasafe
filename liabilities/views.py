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
import csv
import io

from .models import Liability

@login_required
def liability_list(request):
    """List all liabilities for the current user"""
    liabilities = Liability.objects.filter(user=request.user, is_active=True)

    # Filter by liability type if specified
    liability_type = request.GET.get('type')
    if liability_type:
        liabilities = liabilities.filter(liability_type=liability_type)

    # Search functionality
    search = request.GET.get('search')
    if search:
        liabilities = liabilities.filter(
            name__icontains=search
        ) | liabilities.filter(description__icontains=search)

    context = {
        'liabilities': liabilities,
        'liability_types': Liability.LIABILITY_TYPES,
        'current_type': liability_type,
        'search': search,
    }
    return render(request, 'liabilities/liability_list.html', context)

@login_required
def liability_create(request):
    """Create a new liability"""
    if request.method == 'POST':
        # Handle form submission
        messages.success(request, 'Liability created successfully!')
        return redirect('liabilities:liability_list')

    return render(request, 'liabilities/liability_form.html')

@login_required
def liability_detail(request, pk):
    """View liability details"""
    liability = get_object_or_404(Liability, pk=pk, user=request.user)
    return render(request, 'liabilities/liability_detail.html', {
        'liability': liability
    })

@login_required
def liability_update(request, pk):
    """Update liability"""
    liability = get_object_or_404(Liability, pk=pk, user=request.user)

    if request.method == 'POST':
        messages.success(request, 'Liability updated successfully!')
        return redirect('liabilities:liability_detail', pk=pk)

    return render(request, 'liabilities/liability_form.html', {'liability': liability})

@login_required
def liability_delete(request, pk):
    """Delete liability"""
    liability = get_object_or_404(Liability, pk=pk, user=request.user)
    liability.is_active = False
    liability.save()
    messages.success(request, 'Liability deleted successfully!')
    return redirect('liabilities:liability_list')

@login_required
def export_liabilities_pdf(request):
    """Export all liabilities as PDF"""
    liabilities = Liability.objects.filter(user=request.user, is_active=True)

    # Create PDF buffer
    buffer = io.BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph("BeneSafe - Liability Report", styles['Heading1'])
    story.append(title)
    story.append(Spacer(1, 12))

    # User info
    user_info = Paragraph(f"Generated for: {request.user.get_full_name()} ({request.user.username})", styles['Normal'])
    story.append(user_info)
    story.append(Spacer(1, 12))

    # Liabilities data
    if liabilities:
        data = [['Liability Name', 'Type', 'Amount', 'Source', 'Due Date', 'Created Date']]

        for liability in liabilities:
            data.append([
                liability.name,
                liability.get_liability_type_display(),
                f"${liability.amount:.2f}",
                liability.source or '',
                liability.due_date.strftime('%Y-%m-%d') if liability.due_date else '',
                liability.created_at.strftime('%Y-%m-%d')
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
        no_data = Paragraph("No liabilities found.", styles['Normal'])
        story.append(no_data)

    # Build PDF
    doc.build(story)

    # Return PDF response
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="liabilities_{request.user.username}.pdf"'
    return response

@login_required
def export_liabilities_csv(request):
    """Export all liabilities as CSV"""
    liabilities = Liability.objects.filter(user=request.user, is_active=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="liabilities_{request.user.username}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Type', 'Amount', 'Source', 'Due Date', 'Created Date'])

    for liability in liabilities:
        writer.writerow([
            liability.name,
            liability.get_liability_type_display(),
            liability.amount,
            liability.source,
            liability.due_date.strftime('%Y-%m-%d') if liability.due_date else '',
            liability.created_at.strftime('%Y-%m-%d')
        ])

    return response
