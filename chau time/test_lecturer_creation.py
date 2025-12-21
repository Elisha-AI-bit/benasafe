#!/usr/bin/env python
"""
Test script to verify lecturer creation functionality.
"""
import os
import sys
import django

# Add the project directory to the Python path
project_path = r"c:\Users\THE ARCHTECT\Documents\projets2\chau time"
sys.path.insert(0, project_path)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timetable_project.settings')
django.setup()

from timetable.models import User, Lecturer
from timetable.forms import UserForm, LecturerForm

def test_lecturer_creation():
    """Test creating a lecturer with the fixed forms."""

    # Test data
    user_data = {
        'name': 'Test Lecturer',
        'email': f'test.lecturer.{int(__import__("time").time())}@example.com',
        'password': 'testpass123',
        'is_active': True
    }

    lecturer_data = {
        'initials': 'TL',
        'phone': '123456789',
        'office': 'Office 101',
        'specialization': 'Computer Science',
        'monday_available': True,
        'tuesday_available': True,
        'wednesday_available': True,
        'thursday_available': True,
        'friday_available': True,
        'saturday_available': False,
        'sunday_available': False,
        'max_hours_per_week': 20
    }

    try:
        # Test form validation
        user_form = UserForm(user_data)
        lecturer_form = LecturerForm(lecturer_data)

        print(f"User form valid: {user_form.is_valid()}")
        if not user_form.is_valid():
            print(f"User form errors: {user_form.errors}")

        print(f"Lecturer form valid: {lecturer_form.is_valid()}")
        if not lecturer_form.is_valid():
            print(f"Lecturer form errors: {lecturer_form.errors}")

        if user_form.is_valid() and lecturer_form.is_valid():
            # Test saving
            user = user_form.save(commit=False)
            user.role = 'LECTURER'
            print(f"About to save user: {user}")
            print(f"User ID before save: {user.id}")
            user.save()
            print(f"User saved successfully. ID: {user.id}")
            print(f"User email: {user.email}")
            print(f"User name: {user.name}")

            lecturer = lecturer_form.save(commit=False)
            print(f"Lecturer before assigning user: {lecturer}")
            print(f"Lecturer user_id before assignment: {lecturer.user_id}")
            lecturer.user = user
            print(f"Lecturer after assigning user: {lecturer}")
            print(f"Lecturer user_id after assignment: {lecturer.user_id}")
            print(f"Assigned user ID: {user.id}")
            lecturer.save()
            print(f"Lecturer saved successfully: {lecturer}")

            # Cleanup
            lecturer.delete()
            user.delete()

            return True
        else:
            return False

    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_lecturer_creation()
    if success:
        print("\n✅ Test passed! Lecturer creation should work correctly.")
    else:
        print("\n❌ Test failed! There are still issues with lecturer creation.")
