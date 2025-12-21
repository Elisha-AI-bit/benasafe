# Quick Start Guide - Chalimbana University Timetable System

## Get Started in 5 Minutes

### Step 1: Install Dependencies (1 minute)

```bash
cd "c:\Users\THE ARCHTECT\Documents\projets2\chau time"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Setup Database (1 minute)

```bash
python manage.py migrate
python manage.py seed_data
```

### Step 3: Run Server (30 seconds)

```bash
python manage.py runserver
```

### Step 4: Login (30 seconds)

Open browser: `http://127.0.0.1:8000/`

**Admin Login:**
- Email: `admin@chalimbana.edu.zm`
- Password: `admin123`

### Step 5: Generate Timetable (2 minutes)

1. Click **"Schedule"** in navigation
2. Select **"All Programmes"**
3. Check **"Clear existing timetable"**
4. Click **"Generate Timetable"**
5. View results in **"Timetable"** menu

## Common Tasks

### Add a New Lecturer

1. Navigate to **Lecturers** → **Add New Lecturer**
2. Fill in user information (name, email, password)
3. Fill in lecturer details (initials, phone, office)
4. Set availability (check available days)
5. Click **Add Lecturer**

### Add a New Student

1. Navigate to **Students** → **Add New Student**
2. Fill in user information
3. Fill in student details (ID, programme, intake, type)
4. Click **Add Student**

### Add a New Course

1. Navigate to **Courses** → **Add New Course**
2. Enter course code and name
3. Select programme and lecturer
4. Set year, semester, and hours per week
5. Click **Add Course**

### Manual Schedule Entry

1. Navigate to **Timetable** → **Add Entry**
2. Select course, lecturer, classroom
3. Choose programme and intake
4. Set day and time
5. Click **Add Entry**

### Export Timetable

1. Navigate to **Timetable**
2. Apply filters (optional)
3. Click export button:
   - **PDF** for printing
   - **Excel** for editing
   - **HTML** for interactive viewing

### View Conflicts

1. Navigate to **Conflicts** from admin dashboard
2. Review conflict details
3. Click **Edit Entry** to resolve
4. Mark as **Resolved** when fixed

## Tips

- **Always check conflicts** after auto-scheduling
- **Set lecturer availability** before scheduling
- **Verify classroom capacity** matches student numbers
- **Use filters** to view specific programme timetables
- **Export regularly** to keep backup copies

## Troubleshooting

**Can't login?**
- Verify email and password
- Run `python manage.py seed_data` again

**No timetable entries?**
- Ensure courses have assigned lecturers
- Check that classrooms exist
- Run auto-schedule

**Conflicts appearing?**
- Edit conflicting entries manually
- Adjust lecturer availability
- Add more classrooms

## Next Steps

- Read **FEATURES.md** for complete feature list
- Read **INSTALLATION.md** for detailed setup
- Explore the admin dashboard
- Customize for your institution

## Support

For help, check the README.md or contact IT support.
