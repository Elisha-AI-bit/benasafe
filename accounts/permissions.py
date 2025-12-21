"""
Permission utilities for BeneSafe user roles and bouquets
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def require_permission(permission_name):
    """
    Decorator to check if a user has a specific permission
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            # Check if user has the required permission through their profile
            if hasattr(request.user, 'userprofile'):
                if not request.user.userprofile.has_permission(permission_name):
                    messages.error(request, 'You do not have permission to access this page.')
                    raise PermissionDenied("Insufficient permissions")
            else:
                messages.error(request, 'User profile not found.')
                raise PermissionDenied("User profile not found")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_role(role_type):
    """
    Decorator to check if a user has a specific role type
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            if hasattr(request.user, 'userprofile'):
                user_role_type = getattr(request.user.userprofile, f'is_{role_type}', False)
                if not user_role_type:
                    messages.error(request, f'This page is only accessible to {role_type.replace("_", " ").title()} users.')
                    raise PermissionDenied(f"Requires {role_type} role")
            else:
                messages.error(request, 'User profile not found.')
                raise PermissionDenied("User profile not found")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_bouquet_feature(feature_name):
    """
    Decorator to check if a user's bouquet has a specific feature
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            if hasattr(request.user, 'userprofile'):
                if not request.user.userprofile.bouquet:
                    messages.error(request, 'No subscription bouquet assigned.')
                    raise PermissionDenied("No bouquet assigned")
                
                if not getattr(request.user.userprofile.bouquet, feature_name, False):
                    messages.error(request, f'This feature requires a higher subscription tier.')
                    return redirect('accounts:upgrade_bouquet')
            else:
                messages.error(request, 'User profile not found.')
                raise PermissionDenied("User profile not found")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def check_bouquet_limit(model_class, user, category=None):
    """
    Check if user has reached their bouquet limit for a specific model
    Returns True if within limit, False if limit reached
    """
    if not user.userprofile or not user.userprofile.bouquet:
        return False
    
    # Get the current count of items for this user
    if category:
        current_count = model_class.objects.filter(user=user, category=category).count()
        limit = user.userprofile.get_asset_limit(category)
    else:
        current_count = model_class.objects.filter(user=user).count()
        # For beneficiaries, use beneficiary limit
        if 'beneficiar' in model_class.__name__.lower():
            limit = user.userprofile.get_beneficiary_limit()
        elif 'dependent' in model_class.__name__.lower():
            limit = user.userprofile.get_dependent_limit()
        else:
            limit = user.userprofile.get_asset_limit()
    
    return current_count < limit

def get_bouquet_limits(user):
    """
    Get all bouquet limits for a user
    """
    if not user.userprofile or not user.userprofile.bouquet:
        return {}
    
    bouquet = user.userprofile.bouquet
    return {
        'assets_per_category': bouquet.max_assets_per_category,
        'beneficiaries': bouquet.max_beneficiaries,
        'dependents': bouquet.max_dependents,
        'has_reward_tracker': bouquet.has_reward_tracker,
        'reward_percentage': bouquet.reward_percentage,
        'can_export_reports': bouquet.can_export_reports,
        'can_download_documents': bouquet.can_download_documents,
        'can_manage_businesses': bouquet.can_manage_businesses,
        'can_manage_professional_contacts': bouquet.can_manage_professional_contacts,
    }



