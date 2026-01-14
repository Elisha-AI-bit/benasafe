from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def billing_dashboard(request):
    """Billing dashboard"""
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    return render(request, 'billing/dashboard.html')

@login_required
def subscription_list(request):
    """List all subscriptions"""
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    return render(request, 'billing/subscription_list.html')

@login_required
def payment_list(request):
    """List all payments"""
    if request.user.userprofile.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('core:dashboard')

    return render(request, 'billing/payment_list.html')

@login_required
def upgrade_plan(request):
    """Upgrade subscription plan"""
    return render(request, 'billing/upgrade.html')

def initiate_payment(request):
    """View to initiate mobile money payment during registration"""
    user_id = request.session.get('registration_user_id')
    bouquet_id = request.session.get('selected_bouquet_id')

    if not user_id or not bouquet_id:
        messages.error(request, "Registration session expired. Please start again.")
        return redirect('accounts:register')

    from accounts.models import Bouquet
    from django.contrib.auth.models import User
    
    user = get_object_or_404(User, id=user_id)
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)

    if request.method == 'POST':
        # Here we would normally call the mobile money API (e.g., Aggregator)
        # For now, we simulate success when the user clicks "Pay Now"
        return redirect('billing:verify_payment')

    context = {
        'user': user,
        'bouquet': bouquet,
        'mobile_money_options': ['Airtel Money', 'MTN Money', 'Zamtel Kwacha']
    }
    return render(request, 'billing/payment_mobile_money.html', context)

def verify_payment(request):
    """View to verify payment and activate user"""
    user_id = request.session.get('registration_user_id')
    bouquet_id = request.session.get('selected_bouquet_id')

    if not user_id or not bouquet_id:
        messages.error(request, "Session expired.")
        return redirect('accounts:register')

    from django.contrib.auth.models import User
    from accounts.models import Bouquet, UserProfile
    from .models import Payment, Subscription
    from django.contrib.auth import login
    import uuid
    from django.utils import timezone

    user = get_object_or_404(User, id=user_id)
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)

    # Activate user
    user.is_active = True
    user.save()

    # Create/Update Subscription
    subscription, created = Subscription.objects.get_or_create(
        user=user,
        defaults={'plan': bouquet.name, 'is_active': True}
    )
    if not created:
        subscription.plan = bouquet.name
        subscription.is_active = True
        subscription.save()

    # Record Payment
    Payment.objects.create(
        user=user,
        subscription=subscription,
        amount=bouquet.price,
        status='completed',
        reference=f"MOMO-{uuid.uuid4().hex[:8].upper()}",
        payment_date=timezone.now()
    )

    # Update UserProfile if necessary
    profile = user.userprofile
    profile.bouquet = bouquet
    profile.subscription_active = True
    profile.save()

    # Clear session
    del request.session['registration_user_id']
    del request.session['selected_bouquet_id']

    # Log user in
    login(request, user)
    
    messages.success(request, f"Payment successful! Welcome to BeneSafe, {user.username}.")
    return redirect('core:dashboard')
