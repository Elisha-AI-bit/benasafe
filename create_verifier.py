from django.contrib.auth.models import User
from accounts.models import UserProfile, UserRole, Bouquet

def create_verifier():
    username = 'verifier'
    email = 'verifier@benesafe.com'
    password = 'verifier123'
    
    if User.objects.filter(username=username).exists():
        print(f"User {username} already exists.")
        return

    # Create the user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Test',
        last_name='Verifier',
        is_staff=True,
        is_active=True
    )

    # Get Corporate Verifier role
    try:
        verifier_role = UserRole.objects.get(role_type='verifier', sub_role='corporate_verifier')
    except UserRole.DoesNotExist:
        print("Verifier role not found.")
        return

    # Get Blue bouquet
    try:
        blue_bouquet = Bouquet.objects.get(name='blue')
    except Bouquet.DoesNotExist:
        print("Blue bouquet not found.")
        return

    # Create profile
    UserProfile.objects.create(
        user=user,
        role=verifier_role,
        bouquet=blue_bouquet,
        verification_status='approved',
        subscription_active=True
    )
    print(f"Verifier user created: {username} / {password}")

if __name__ == "__main__":
    create_verifier()
