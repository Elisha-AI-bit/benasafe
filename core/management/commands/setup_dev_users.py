from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserRole, Bouquet

class Command(BaseCommand):
    help = 'Create a superuser and test user for BeneSafe development'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser...')
            superuser = User.objects.create_superuser(
                username='admin',
                email='admin@benesafe.com',
                password='admin123',
                first_name='System',
                last_name='Administrator'
            )

            # Get admin role and gold bouquet
            try:
                super_admin_role = UserRole.objects.get(name='SuperAdmin')
                gold_bouquet = Bouquet.objects.get(name='gold')
            except (UserRole.DoesNotExist, Bouquet.DoesNotExist):
                self.stdout.write(
                    self.style.ERROR('Required roles/bouquets not found! Please run setup_roles_and_bouquets first.')
                )
                return

            # Create or update profile with proper role and bouquet
            profile, created = UserProfile.objects.get_or_create(
                user=superuser,
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
                self.style.SUCCESS(f'Superuser created: admin/admin123')
            )

        # Create test user
        if not User.objects.filter(username='testuser').exists():
            self.stdout.write('Creating test user...')
            testuser = User.objects.create_user(
                username='testuser',
                email='test@benesafe.com',
                password='test123',
                first_name='Test',
                last_name='User'
            )

            # Get standard role and blue bouquet
            try:
                standard_role = UserRole.objects.get(role_type='standard', is_active=True)
                blue_bouquet = Bouquet.objects.get(name='blue', is_active=True)
            except (UserRole.DoesNotExist, Bouquet.DoesNotExist):
                self.stdout.write(
                    self.style.ERROR('Required roles/bouquets not found! Please run setup_roles_and_bouquets first.')
                )
                return

            # Create or update profile with proper role and bouquet
            profile, created = UserProfile.objects.get_or_create(
                user=testuser,
                defaults={
                    'role': standard_role,
                    'bouquet': blue_bouquet,
                    'phone': '+260123456789',
                    'nrc': '123456/78/9',
                    'verification_status': 'approved',
                    'is_email_verified': True,
                    'subscription_active': True,
                }
            )

            if not created:
                profile.role = standard_role
                profile.bouquet = blue_bouquet
                profile.phone = '+260123456789'
                profile.nrc = '123456/78/9'
                profile.verification_status = 'approved'
                profile.is_email_verified = True
                profile.subscription_active = True
                profile.save()

            self.stdout.write(
                self.style.SUCCESS(f'Test user created: testuser/test123')
            )

        self.stdout.write(
            self.style.SUCCESS('Development users created successfully!')
        )
