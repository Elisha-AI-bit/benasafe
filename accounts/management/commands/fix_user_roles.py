from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserRole, Bouquet

class Command(BaseCommand):
    help = 'Fix user roles and bouquets for existing users'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Specific username to fix')
        parser.add_argument('--all', action='store_true', help='Fix all users')

    def handle(self, *args, **options):
        self.stdout.write('Fixing user roles and bouquets...')
        
        # Get default role and bouquet
        try:
            standard_role = UserRole.objects.get(role_type='standard', is_active=True)
            blue_bouquet = Bouquet.objects.get(name='blue', is_active=True)
        except (UserRole.DoesNotExist, Bouquet.DoesNotExist):
            self.stdout.write(
                self.style.ERROR('Default role or bouquet not found! Please run setup_roles_and_bouquets first.')
            )
            return
        
        if options['username']:
            # Fix specific user
            try:
                user = User.objects.get(username=options['username'])
                self.fix_user(user, standard_role, blue_bouquet)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User {options["username"]} not found!')
                )
        elif options['all']:
            # Fix all users
            users = User.objects.all()
            for user in users:
                self.fix_user(user, standard_role, blue_bouquet)
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --username <username> or --all')
            )

    def fix_user(self, user, standard_role, blue_bouquet):
        """Fix a single user's role and bouquet"""
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            self.stdout.write(f'Creating profile for {user.username}...')
            try:
                profile = UserProfile.objects.create(
                    user=user,
                    role=standard_role,
                    bouquet=blue_bouquet
                )
            except Exception as e:
                self.stdout.write(f'Error creating profile for {user.username}: {e}')
                # Fallback: try without role/bouquet
                profile = UserProfile.objects.create(user=user)
        
        updated = False
        
        if not profile.role:
            profile.role = standard_role
            updated = True
            self.stdout.write(f'Assigned role to {user.username}')
        
        if not profile.bouquet:
            profile.bouquet = blue_bouquet
            updated = True
            self.stdout.write(f'Assigned bouquet to {user.username}')
        
        if updated:
            profile.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated {user.username}')
            )
        else:
            self.stdout.write(f'{user.username} already configured')


