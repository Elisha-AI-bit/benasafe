from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.contrib.auth.models import User
from assets.models import Asset
from accounts.models import UserProfile, Bouquet, UserRole

def dashboard(request):
    """Main dashboard view - routes to role-specific dashboards"""
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create a default profile with standard role for users who don't have one
        try:
            standard_role = UserRole.objects.get(role_type='standard', is_active=True)
            blue_bouquet = Bouquet.objects.get(name='blue', is_active=True)
            profile = UserProfile.objects.create(
                user=request.user,
                role=standard_role,
                bouquet=blue_bouquet
            )
        except (UserRole.DoesNotExist, Bouquet.DoesNotExist):
            # Fallback: create profile without role/bouquet if defaults don't exist
            profile = UserProfile.objects.create(user=request.user)

    # If user doesn't have a role or bouquet, show a setup page
    if not profile.role or not profile.bouquet:
        # For now, show the standard dashboard but with a warning
        messages.warning(request, 'Your account is not fully configured. Some features may be limited.')
        return standard_user_dashboard(request)

    # Route to appropriate dashboard based on role
    if profile.is_admin:
        return admin_dashboard(request)
    elif profile.is_verifier:
        return verifier_dashboard(request)
    else:
        return standard_user_dashboard(request)

def standard_user_dashboard(request):
    """Standard user dashboard"""
    # Get dashboard statistics
    total_assets = Asset.objects.filter(user=request.user, is_active=True).count()
    total_liabilities = 0  # Will be implemented when liabilities app is ready
    total_documents = 0  # Will be implemented when documents app is ready

    # Calculate net worth (assets - liabilities)
    asset_value = Asset.objects.filter(user=request.user, is_active=True).aggregate(
        total=Sum('value')
    )['total'] or 0

    net_worth = asset_value - total_liabilities

    # Get recent assets
    recent_assets = Asset.objects.filter(user=request.user, is_active=True)[:5]

    # Get profile safely
    try:
        profile = request.user.userprofile
    except:
        profile = None

    context = {
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'net_worth': net_worth,
        'total_documents': total_documents,
        'recent_assets': recent_assets,
        'user': request.user,
        'profile': profile,
        'dashboard_type': 'standard',
    }
    return render(request, 'core/dashboard.html', context)

def admin_dashboard(request):
    """Admin dashboard with system-wide statistics"""
    profile = request.user.userprofile
    
    # System-wide statistics
    total_users = User.objects.filter(is_active=True).count()
    total_assets = Asset.objects.filter(is_active=True).count()
    pending_verifications = UserProfile.objects.filter(verification_status='pending').count()
    active_subscriptions = UserProfile.objects.filter(subscription_active=True).count()
    
    # Revenue calculation (simplified)
    revenue_data = []
    for bouquet in Bouquet.objects.filter(is_active=True):
        count = UserProfile.objects.filter(bouquet=bouquet, subscription_active=True).count()
        revenue = count * bouquet.price
        revenue_data.append({
            'bouquet': bouquet,
            'count': count,
            'revenue': revenue
        })
    
    total_revenue = sum(item['revenue'] for item in revenue_data)
    
    # Recent user registrations
    recent_users = User.objects.filter(is_active=True).order_by('-date_joined')[:10]
    
    # Users by bouquet
    users_by_bouquet = {}
    for bouquet in Bouquet.objects.filter(is_active=True):
        users_by_bouquet[bouquet.name] = UserProfile.objects.filter(
            bouquet=bouquet, subscription_active=True
        ).count()
    
    # Recent assets across all users
    recent_assets = Asset.objects.filter(is_active=True).order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_assets': total_assets,
        'pending_verifications': pending_verifications,
        'active_subscriptions': active_subscriptions,
        'total_revenue': total_revenue,
        'revenue_data': revenue_data,
        'recent_users': recent_users,
        'users_by_bouquet': users_by_bouquet,
        'recent_assets': recent_assets,
        'user': request.user,
        'profile': profile,
        'dashboard_type': 'admin',
    }
    return render(request, 'core/admin_dashboard.html', context)

def verifier_dashboard(request):
    """Verifier dashboard for document verification tasks"""
    profile = request.user.userprofile
    
    # Verification statistics
    pending_verifications = UserProfile.objects.filter(verification_status='pending').count()
    approved_verifications = UserProfile.objects.filter(verification_status='approved').count()
    rejected_verifications = UserProfile.objects.filter(verification_status='rejected').count()
    
    # Recent pending verifications
    recent_pending = UserProfile.objects.filter(
        verification_status='pending'
    ).order_by('-created_at')[:10]
    
    # Recent verification history
    recent_verifications = UserProfile.objects.filter(
        verification_status__in=['approved', 'rejected']
    ).order_by('-updated_at')[:10]

    context = {
        'pending_verifications': pending_verifications,
        'approved_verifications': approved_verifications,
        'rejected_verifications': rejected_verifications,
        'recent_pending': recent_pending,
        'recent_verifications': recent_verifications,
        'user': request.user,
        'profile': profile,
        'dashboard_type': 'verifier',
    }
    return render(request, 'core/verifier_dashboard.html', context)

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('accounts:login')

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        # Handle registration logic here
        messages.info(request, 'Registration functionality will be implemented')
        return redirect('accounts:login')

    return render(request, 'accounts/register.html')
