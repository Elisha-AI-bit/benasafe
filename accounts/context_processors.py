"""
Context processors for BeneSafe accounts app
"""
from .models import Bouquet

def user_profile_context(request):
    """
    Add user profile information to template context
    """
    context = {}
    
    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        profile = request.user.userprofile
        context.update({
            'user_profile': profile,
            'user_role': profile.role,
            'user_bouquet': profile.bouquet,
            'is_admin': profile.is_admin,
            'is_verifier': profile.is_verifier,
            'is_standard_user': profile.is_standard_user,
            'is_super_admin': profile.is_super_admin,
            'verification_status': profile.verification_status,
            'subscription_active': profile.subscription_active,
        })
        
        # Add bouquet limits if bouquet exists
        if profile.bouquet:
            context.update({
                'asset_limit': profile.get_asset_limit(),
                'beneficiary_limit': profile.get_beneficiary_limit(),
                'dependent_limit': profile.get_dependent_limit(),
                'has_reward_tracker': profile.bouquet.has_reward_tracker,
                'reward_percentage': profile.bouquet.reward_percentage,
            })
    
    return context

def bouquet_options(request):
    """
    Add bouquet options to template context for upgrade/registration forms
    """
    context = {}
    
    # Get active bouquets for forms
    active_bouquets = Bouquet.objects.filter(is_active=True).order_by('price')
    context['available_bouquets'] = active_bouquets
    
    return context



