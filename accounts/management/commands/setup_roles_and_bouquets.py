from django.core.management.base import BaseCommand
from accounts.models import UserRole, Bouquet

class Command(BaseCommand):
    help = 'Set up initial user roles and bouquets for BeneSafe system'

    def handle(self, *args, **options):
        self.stdout.write('Setting up BeneSafe user roles and bouquets...')
        
        # Create Bouquets
        self.create_bouquets()
        
        # Create User Roles
        self.create_user_roles()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up all roles and bouquets!')
        )

    def create_bouquets(self):
        """Create the three subscription bouquets: Blue, Red, Gold"""
        bouquets_data = [
            {
                'name': 'blue',
                'display_name': 'Blue Bouquet',
                'description': 'Basic subscription plan with limited features',
                'price': 100.00,
                'max_assets_per_category': 3,
                'max_dependents': 1,
                'max_beneficiaries': 3,
                'has_reward_tracker': False,
                'reward_percentage': 0,
                'can_export_reports': True,
                'can_download_documents': True,
                'can_manage_businesses': True,
                'can_manage_professional_contacts': True,
            },
            {
                'name': 'red',
                'display_name': 'Red Bouquet',
                'description': 'Standard subscription plan with extended features',
                'price': 250.00,
                'max_assets_per_category': 6,
                'max_dependents': 3,
                'max_beneficiaries': 5,
                'has_reward_tracker': False,
                'reward_percentage': 0,
                'can_export_reports': True,
                'can_download_documents': True,
                'can_manage_businesses': True,
                'can_manage_professional_contacts': True,
            },
            {
                'name': 'gold',
                'display_name': 'Gold Bouquet',
                'description': 'Premium subscription plan with unlimited features and reward tracker',
                'price': 500.00,
                'max_assets_per_category': 999,  # Unlimited
                'max_dependents': 999,  # Unlimited
                'max_beneficiaries': 999,  # Unlimited
                'has_reward_tracker': True,
                'reward_percentage': 30,
                'can_export_reports': True,
                'can_download_documents': True,
                'can_manage_businesses': True,
                'can_manage_professional_contacts': True,
            }
        ]

        for bouquet_data in bouquets_data:
            bouquet, created = Bouquet.objects.get_or_create(
                name=bouquet_data['name'],
                defaults=bouquet_data
            )
            if created:
                self.stdout.write(f'Created bouquet: {bouquet.display_name}')
            else:
                self.stdout.write(f'Bouquet already exists: {bouquet.display_name}')

    def create_user_roles(self):
        """Create user roles for Admin, Verifier, and Standard users"""
        roles_data = [
            # Admin Roles
            {
                'name': 'SuperAdmin',
                'role_type': 'admin',
                'sub_role': 'super_admin',
                'description': 'Full system control with backend and frontend access',
                'can_manage_users': True,
                'can_assign_bouquets': True,
                'can_view_all_data': True,
                'can_manage_payments': True,
                'can_manage_verification': True,
                'can_export_reports': True,
                'can_approve_documents': True,
                'can_send_notifications': True,
            },
            {
                'name': 'Admin Staff',
                'role_type': 'admin',
                'sub_role': 'admin_staff',
                'description': 'Handles user management, bouquet setup, and general system configuration',
                'can_manage_users': True,
                'can_assign_bouquets': True,
                'can_view_all_data': True,
                'can_manage_payments': True,
                'can_manage_verification': True,
                'can_export_reports': True,
                'can_approve_documents': True,
                'can_send_notifications': True,
            },
            # Verifier Roles
            {
                'name': 'Corporate Verifier',
                'role_type': 'verifier',
                'sub_role': 'corporate_verifier',
                'description': 'Reviews ownership and business-related documents',
                'can_view_pending_verifications': True,
                'can_review_approve': True,
                'can_download_documents': True,
                'can_upload_verification_report': True,
                'can_maintain_audit_log': True,
                'can_notify_users': True,
            },
            {
                'name': 'Legal Verifier',
                'role_type': 'verifier',
                'sub_role': 'legal_verifier',
                'description': 'Reviews personal identity, legal, and property documents',
                'can_view_pending_verifications': True,
                'can_review_approve': True,
                'can_download_documents': True,
                'can_upload_verification_report': True,
                'can_maintain_audit_log': True,
                'can_notify_users': True,
            },
            # Standard User Role
            {
                'name': 'Standard User',
                'role_type': 'standard',
                'sub_role': '',
                'description': 'Everyday BeneSafe users with bouquet-based permissions',
                'can_add_edit_personal_details': True,
                'can_add_spouse_dependents': True,
                'can_upload_documents': True,
                'can_manage_assets': True,
                'can_manage_liabilities': True,
                'can_manage_businesses': True,
                'can_manage_professional_contacts': True,
                'can_add_beneficiaries': True,
                'can_view_dashboard': True,
                'can_receive_verification_updates': True,
            }
        ]

        for role_data in roles_data:
            role, created = UserRole.objects.get_or_create(
                name=role_data['name'],
                defaults=role_data
            )
            if created:
                self.stdout.write(f'Created role: {role.name} ({role.get_role_type_display()})')
            else:
                self.stdout.write(f'Role already exists: {role.name}')

