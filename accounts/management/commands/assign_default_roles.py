from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserRole, Bouquet

class Command(BaseCommand):
    help = 'Assign default roles and bouquets to users who don\'t have them'

    def handle(self, *args, **options):
        self.stdout.write('Assigning default roles and bouquets to users...')
        
        # Get default role and bouquet
        try:
            standard_role = UserRole.objects.get(role_type='standard', is_active=True)
            blue_bouquet = Bouquet.objects.get(name='blue', is_active=True)
        except (UserRole.DoesNotExist, Bouquet.DoesNotExist):
            self.stdout.write(
                self.style.ERROR('Default role or bouquet not found! Please run setup_roles_and_bouquets first.')
            )
            return
        
        # Get all users without profiles
        users_without_profiles = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profiles:
            try:
                profile = UserProfile.objects.create(
                    user=user,
                    role=standard_role,
                    bouquet=blue_bouquet
                )
                self.stdout.write(f'Created profile for user: {user.username}')
            except Exception as e:
                self.stdout.write(f'Error creating profile for {user.username}: {e}')
                # Fallback: try without role/bouquet
                profile = UserProfile.objects.create(user=user)
        
        # Get all profiles without roles
        profiles_without_roles = UserProfile.objects.filter(role__isnull=True)
        for profile in profiles_without_roles:
            profile.role = standard_role
            profile.save()
            self.stdout.write(f'Assigned role to user: {profile.user.username}')
        
        # Get all profiles without bouquets
        profiles_without_bouquets = UserProfile.objects.filter(bouquet__isnull=True)
        for profile in profiles_without_bouquets:
            profile.bouquet = blue_bouquet
            profile.save()
            self.stdout.write(f'Assigned bouquet to user: {profile.user.username}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully assigned default roles and bouquets!')
        )
