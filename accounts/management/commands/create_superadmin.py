from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserRole, Bouquet

class Command(BaseCommand):
    help = 'Create a super admin user for BeneSafe system'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Username for super admin')
        parser.add_argument('--email', type=str, default='admin@benesafe.com', help='Email for super admin')
        parser.add_argument('--password', type=str, default='admin123', help='Password for super admin')
        parser.add_argument('--first-name', type=str, default='Super', help='First name for super admin')
        parser.add_argument('--last-name', type=str, default='Admin', help='Last name for super admin')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User with username "{username}" already exists!')
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email "{email}" already exists!')
            )
            return

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        # Get or create SuperAdmin role
        try:
            super_admin_role = UserRole.objects.get(name='SuperAdmin')
        except UserRole.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('SuperAdmin role not found! Please run setup_roles_and_bouquets first.')
            )
            return

        # Get or create Gold bouquet (for admin users)
        try:
            gold_bouquet = Bouquet.objects.get(name='gold')
        except Bouquet.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Gold bouquet not found! Please run setup_roles_and_bouquets first.')
            )
            return

        # Create or update user profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': super_admin_role,
                'bouquet': gold_bouquet,
                'verification_status': 'approved',
                'is_email_verified': True,
                'subscription_active': True,
            }
        )

        if not created:
            profile.role = super_admin_role
            profile.bouquet = gold_bouquet
            profile.verification_status = 'approved'
            profile.is_email_verified = True
            profile.subscription_active = True
            profile.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created SuperAdmin user:\n'
                f'Username: {username}\n'
                f'Email: {email}\n'
                f'Password: {password}\n'
                f'Role: {super_admin_role.name}\n'
                f'Bouquet: {gold_bouquet.display_name}'
            )
        )

