from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import csv
import json
import io

from .models import (
    Asset, BankAccount, Insurance, VillageBankingGroup,
    HouseLand, MotorVehicle, Project, GeneralAsset,
    TreasuryBond, IPRights, AssetDocument
)
from .forms import (
    BankAccountForm, InsuranceForm, VillageBankingForm,
    HouseLandForm, MotorVehicleForm, ProjectForm,
    GeneralAssetForm, TreasuryBondForm, IPRightsForm,
    AssetDocumentForm
)

@login_required
def asset_list(request):
    """List all assets for the current user"""
    assets = Asset.objects.filter(user=request.user, is_active=True)

    # Filter by asset type if specified
    asset_type = request.GET.get('type')
    if asset_type:
        assets = assets.filter(asset_type=asset_type)

    # Search functionality
    search = request.GET.get('search')
    if search:
        assets = assets.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'assets': assets,
        'asset_types': Asset.ASSET_TYPES,
        'current_type': asset_type,
        'search': search,
    }
    return render(request, 'assets/asset_list.html', context)

@login_required
def bank_account_list(request):
    """List all bank accounts"""
    assets = Asset.objects.filter(user=request.user, asset_type='bank_account', is_active=True)
    return render(request, 'assets/bank_account_list.html', {'assets': assets})

@login_required
def bank_account_create(request):
    """Create a new bank account"""
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            asset.asset_type = 'bank_account'
            asset.save()

            # Create the specific bank account details
            BankAccount.objects.create(asset=asset, **form.cleaned_data)

            messages.success(request, 'Bank account added successfully!')
            return redirect('assets:bank_account_list')
    else:
        form = BankAccountForm()

    return render(request, 'assets/bank_account_form.html', {'form': form})

@login_required
def bank_account_detail(request, pk):
    """View bank account details"""
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    bank_account = get_object_or_404(BankAccount, asset=asset)
    return render(request, 'assets/bank_account_detail.html', {
        'asset': asset,
        'bank_account': bank_account
    })

@login_required
def bank_account_update(request, pk):
    """Update bank account"""
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    bank_account = get_object_or_404(BankAccount, asset=asset)

    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            # Update bank account specific fields
            for field, value in form.cleaned_data.items():
                if hasattr(bank_account, field):
                    setattr(bank_account, field, value)
            bank_account.save()

            messages.success(request, 'Bank account updated successfully!')
            return redirect('assets:bank_account_detail', pk=pk)
    else:
        form = BankAccountForm(instance=asset, initial={
            'bank_name': bank_account.bank_name,
            'branch_name': bank_account.branch_name,
            'account_name': bank_account.account_name,
            'account_number': bank_account.account_number,
            'account_type': bank_account.account_type,
        })

    return render(request, 'assets/bank_account_form.html', {'form': form, 'asset': asset})

@login_required
def bank_account_delete(request, pk):
    """Delete bank account"""
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    asset.is_active = False
    asset.save()
    messages.success(request, 'Bank account deleted successfully!')
    return redirect('assets:bank_account_list')

# Similar views for other asset types
@login_required
def insurance_list(request):
    """List all insurance policies"""
    assets = Asset.objects.filter(user=request.user, asset_type='insurance', is_active=True)
    return render(request, 'assets/insurance_list.html', {'assets': assets})

@login_required
def insurance_create(request):
    """Create a new insurance policy"""
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            asset.asset_type = 'insurance'
            asset.save()

            Insurance.objects.create(asset=asset, **form.cleaned_data)

            messages.success(request, 'Insurance policy added successfully!')
            return redirect('assets:insurance_list')
    else:
        form = InsuranceForm()

    return render(request, 'assets/insurance_form.html', {'form': form})

@login_required
def insurance_detail(request, pk):
    """View insurance details"""
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    insurance = get_object_or_404(Insurance, asset=asset)
    return render(request, 'assets/insurance_detail.html', {
        'asset': asset,
        'insurance': insurance
    })

@login_required
def insurance_update(request, pk):
    """Update insurance"""
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    insurance = get_object_or_404(Insurance, asset=asset)

    if request.method == 'POST':
        form = InsuranceForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            # Update insurance specific fields
            for field, value in form.cleaned_data.items():
                if hasattr(insurance, field):
                    setattr(insurance, field, value)
            insurance.save()

            messages.success(request, 'Insurance updated successfully!')
            return redirect('assets:insurance_detail', pk=pk)
    else:
        form = InsuranceForm(instance=asset, initial={
            'policy_number': insurance.policy_number,
            'provider_name': insurance.provider_name,
            'coverage_type': insurance.coverage_type,
            'premium_amount': insurance.premium_amount,
            'maturity_date': insurance.maturity_date,
        })

    return render(request, 'assets/insurance_form.html', {'form': form, 'asset': asset})

@login_required
def insurance_delete(request, pk):
    """Delete insurance"""
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    asset.is_active = False
    asset.save()
    messages.success(request, 'Insurance deleted successfully!')
    return redirect('assets:insurance_list')

@login_required
def asset_document_upload(request, pk):
    """Upload document for asset"""
    asset = get_object_or_404(Asset, pk=pk, user=request.user)

    if request.method == 'POST':
        form = AssetDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.asset = asset
            document.file_type = form.cleaned_data['file'].name.split('.')[-1].lower()
            document.file_size = form.cleaned_data['file'].size
            document.save()

            messages.success(request, 'Document uploaded successfully!')
            return redirect('assets:asset_documents', pk=pk)
    else:
        form = AssetDocumentForm()

    return render(request, 'assets/document_upload.html', {
        'form': form,
        'asset': asset
    })

@login_required
def asset_document_delete(request, pk):
    """Delete asset document"""
    document = get_object_or_404(AssetDocument, pk=pk, asset__user=request.user)
    asset_pk = document.asset.pk
    document.delete()
    messages.success(request, 'Document deleted successfully!')
    return redirect('assets:asset_documents', pk=asset_pk)

@login_required
def asset_documents(request, pk):
    """View and manage asset documents"""
    asset = get_object_or_404(Asset, pk=pk, user=request.user)

    if request.method == 'POST':
        form = AssetDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.asset = asset
            document.file_type = form.cleaned_data['file'].name.split('.')[-1].lower()
            document.file_size = form.cleaned_data['file'].size
            document.save()

            messages.success(request, 'Document uploaded successfully!')
            return redirect('assets:asset_documents', pk=pk)
    else:
        form = AssetDocumentForm()

    documents = AssetDocument.objects.filter(asset=asset)
    return render(request, 'assets/asset_documents.html', {
        'asset': asset,
        'documents': documents,
        'form': form
    })

@login_required
def export_assets_pdf(request):
    """Export all assets as PDF"""
    assets = Asset.objects.filter(user=request.user, is_active=True)

    # Create PDF buffer
    buffer = io.BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph("BeneSafe - Asset Report", styles['Heading1'])
    story.append(title)
    story.append(Spacer(1, 12))

    # User info
    user_info = Paragraph(f"Generated for: {request.user.get_full_name()} ({request.user.username})", styles['Normal'])
    story.append(user_info)
    story.append(Spacer(1, 12))

    # Assets data
    if assets:
        data = [['Asset Name', 'Type', 'Value', 'Created Date']]

        for asset in assets:
            data.append([
                asset.name,
                asset.get_asset_type_display(),
                f"${asset.value or 0:.2f}",
                asset.created_at.strftime('%Y-%m-%d')
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
        no_data = Paragraph("No assets found.", styles['Normal'])
        story.append(no_data)

    # Build PDF
    doc.build(story)

    # Return PDF response
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="assets_{request.user.username}.pdf"'
    return response

@login_required
def export_assets_csv(request):
    """Export all assets as CSV"""
    assets = Asset.objects.filter(user=request.user, is_active=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="assets_{request.user.username}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Type', 'Description', 'Value', 'Created Date'])

    for asset in assets:
        writer.writerow([
            asset.name,
            asset.get_asset_type_display(),
            asset.description,
            asset.value,
            asset.created_at.strftime('%Y-%m-%d')
        ])

    return response

@login_required
def motor_vehicle_list(request):
    """List all motor vehicles"""
    vehicles = MotorVehicle.objects.filter(asset__user=request.user, asset__is_active=True).select_related('asset')
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        vehicles = vehicles.filter(
            Q(asset__name__icontains=search) |
            Q(make__icontains=search) |
            Q(model__icontains=search) |
            Q(registration_number__icontains=search)
        )
    
    context = {
        'vehicles': vehicles,
        'search': search,
    }
    return render(request, 'assets/motor_vehicle_list.html', context)

@login_required
def motor_vehicle_create(request):
    """Create new motor vehicle"""
    if request.method == 'POST':
        form = MotorVehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.asset.user = request.user
            vehicle.asset.asset_type = 'motor_vehicle'
            vehicle.asset.save()
            vehicle.save()
            messages.success(request, 'Motor vehicle added successfully!')
            return redirect('assets:motor_vehicle_list')
    else:
        form = MotorVehicleForm()
    
    return render(request, 'assets/motor_vehicle_form.html', {'form': form, 'title': 'Add Motor Vehicle'})

@login_required
def house_land_list(request):
    """List all house and land properties"""
    properties = HouseLand.objects.filter(asset__user=request.user, asset__is_active=True).select_related('asset')
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        properties = properties.filter(
            Q(asset__name__icontains=search) |
            Q(physical_address__icontains=search) |
            Q(plot_number__icontains=search) |
            Q(title_deed_number__icontains=search)
        )
    
    context = {
        'properties': properties,
        'search': search,
    }
    return render(request, 'assets/house_land_list.html', context)

@login_required
def house_land_create(request):
    """Create new house and land property"""
    if request.method == 'POST':
        form = HouseLandForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.asset.user = request.user
            property_obj.asset.asset_type = 'house_land'
            property_obj.asset.save()
            property_obj.save()
            messages.success(request, 'Property added successfully!')
            return redirect('assets:house_land_list')
    else:
        form = HouseLandForm()
    
    return render(request, 'assets/house_land_form.html', {'form': form, 'title': 'Add Property'})

@login_required
def project_list(request):
    """List all projects"""
    projects = Project.objects.filter(asset__user=request.user, asset__is_active=True).select_related('asset')
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        projects = projects.filter(
            Q(asset__name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(contact_email__icontains=search) |
            Q(progress_status__icontains=search)
        )
    
    context = {
        'projects': projects,
        'search': search,
    }
    return render(request, 'assets/project_list.html', context)

@login_required
def project_create(request):
    """Create new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.asset.user = request.user
            project.asset.asset_type = 'project'
            project.asset.save()
            project.save()
            messages.success(request, 'Project added successfully!')
            return redirect('assets:project_list')
    else:
        form = ProjectForm()
    
    return render(request, 'assets/project_form.html', {'form': form, 'title': 'Add Project'})
