from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from .models import UserProfile, UserRole, Bouquet
from .forms import RegistrationForm, ProfileForm, AdminUserForm, LoginForm
from .permissions import require_permission, require_role

def custom_login(request):
    """Custom login view with proper form handling"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('core:dashboard')
                else:
                    messages.error(request, 'Your account has been deactivated. Please contact support.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            
            # Store registration data in session
            request.session['registration_user_id'] = user.id
            request.session['selected_bouquet_id'] = form.cleaned_data['bouquet'].id
            
            messages.info(request, 'Please complete the payment to activate your account.')
            return redirect('billing:initiate_payment')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def resend_verification_email(request):
    """Resend verification email"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            send_verification_email(request, user)
            messages.success(request, 'Verification email sent! Please check your email.')
            return redirect('accounts:login')
        except User.DoesNotExist:
            messages.error(request, 'No unverified account found with that email address.')
            return redirect('accounts:resend_verification')

    return render(request, 'accounts/resend_verification.html')

def send_verification_email(request, user):
    """Send email verification"""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_link = request.build_absolute_uri(f'/accounts/verify/{uid}/{token}/')

    subject = 'Verify your BeneSafe account'
    message = render_to_string('accounts/email_verification.html', {
        'user': user,
        'verification_link': verification_link,
    })

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

@login_required
def profile(request):
    """User profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile
    })

def verify_email(request, uidb64, token):
    """Email verification view"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        # Get or create the user profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.is_email_verified = True
        profile.save()
        user.save()
        messages.success(request, 'Email verified successfully! You can now log in.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Email verification link is invalid or has expired.')
        return redirect('accounts:register')

# Admin Views
@login_required
@require_permission('can_manage_users')
def admin_user_list(request):
    """Admin view to list and manage users"""
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    bouquet_filter = request.GET.get('bouquet', '')
    
    # Get all user profiles with related data
    users = UserProfile.objects.select_related('user', 'role', 'bouquet').all()
    
    # Apply filters
    if search_query:
        users = users.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
    
    if role_filter:
        users = users.filter(role__id=role_filter)
    
    if bouquet_filter:
        users = users.filter(bouquet__id=bouquet_filter)
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    roles = UserRole.objects.filter(is_active=True)
    bouquets = Bouquet.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'bouquet_filter': bouquet_filter,
        'roles': roles,
        'bouquets': bouquets,
    }
    
    return render(request, 'accounts/admin_user_list.html', context)

@login_required
@require_permission('can_manage_users')
def admin_user_edit(request, user_id):
    """Admin view to edit user details"""
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated successfully!')
            return redirect('accounts:admin_user_list')
    else:
        form = AdminUserForm(instance=profile)
    
    context = {
        'form': form,
        'user': user,
        'profile': profile,
    }
    
    return render(request, 'accounts/admin_user_edit.html', context)

@login_required
@require_permission('can_manage_users')
def admin_user_toggle_status(request, user_id):
    """Admin view to toggle user active status"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User {user.username} has been {status}!')
    
    return redirect('accounts:admin_user_list')

@login_required
@require_permission('can_assign_bouquets')
def admin_bouquet_management(request):
    """Admin view to manage bouquets"""
    bouquets = Bouquet.objects.filter(is_active=True)
    
    context = {
        'bouquets': bouquets,
    }
    
    return render(request, 'accounts/admin_bouquet_management.html', context)

@login_required
@require_permission('can_manage_verification')
def admin_verification_queue(request):
    """Admin view to manage verification queue"""
    pending_users = UserProfile.objects.filter(
        verification_status='pending'
    ).select_related('user', 'bouquet').order_by('-created_at')
    
    context = {
        'pending_users': pending_users,
    }
    
    return render(request, 'accounts/admin_verification_queue.html', context)

@login_required
@require_permission('can_approve_documents')
def admin_verify_user(request, user_id):
    """Admin view to verify/reject user"""
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            profile.verification_status = 'approved'
            profile.save()
            messages.success(request, f'User {user.username} has been approved!')
        elif action == 'reject':
            profile.verification_status = 'rejected'
            profile.save()
            messages.success(request, f'User {user.username} has been rejected!')
    
    return redirect('accounts:admin_verification_queue')
