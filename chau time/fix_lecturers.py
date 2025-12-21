from timetable.models import User, Lecturer

# Get all users with role LECTURER
users = User.objects.filter(role='LECTURER')
print(f'Found {users.count()} users with LECTURER role')

# Create lecturer profiles for any that don't have them
i = 1
for user in users:
    try:
        lecturer = Lecturer.objects.get(user=user)
        print(f'{i}. {user.name} - Profile already exists')
    except Lecturer.DoesNotExist:
        lecturer = Lecturer.objects.create(
            user=user,
            initials=f'L{i:02d}'
        )
        print(f'{i}. {user.name} - Profile created')
    i += 1

print('Done')