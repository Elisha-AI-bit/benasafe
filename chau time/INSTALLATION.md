# Chalimbana University Timetable System - Installation Guide

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git (optional, for version control)

## Step-by-Step Installation

### 1. Navigate to Project Directory

```bash
cd "c:\Users\THE ARCHTECT\Documents\projets2\chau time"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed Database with Sample Data

```bash
python manage.py seed_data
```

This will create:
- Admin user
- Sample schools, programmes, and intakes
- Sample lecturers
- Sample classrooms
- Sample courses
- Sample students

### 7. Create Superuser (Optional)

If you want to create a custom admin account:

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files (For Production)

```bash
python manage.py collectstatic
```

### 9. Run Development Server

```bash
python manage.py runserver
```

### 10. Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

## Default Login Credentials

After running `seed_data`, you can login with:

### Administrator
- **Email:** admin@chalimbana.edu.zm
- **Password:** admin123

### Lecturer
- **Email:** j.mwansa@chalimbana.edu.zm
- **Password:** lecturer123

### Student (Regular)
- **Email:** alice.mulenga@student.chalimbana.edu.zm
- **Password:** student123

### Student (Distance)
- **Email:** daniel.mwape@student.chalimbana.edu.zm
- **Password:** student123

## Quick Start Guide

### For Administrators

1. **Login** with admin credentials
2. **Add Resources:**
   - Navigate to "Lecturers" to add teaching staff
   - Navigate to "Students" to add students
   - Navigate to "Courses" to add courses
   - Navigate to "Classrooms" to add venues
3. **Generate Timetable:**
   - Go to "Schedule" → "Auto Schedule"
   - Select schedule type (All Programmes, Specific Intake, or Specific Programme)
   - Click "Generate Timetable"
4. **View & Export:**
   - Navigate to "Timetable" to view generated schedule
   - Use export buttons to download PDF, Excel, or HTML versions

### For Lecturers

1. **Login** with lecturer credentials
2. **View Dashboard** to see:
   - Personal timetable
   - Assigned courses
3. **Update Availability:**
   - Click "Update Availability"
   - Select available days
   - Set maximum hours per week

### For Students

1. **Login** with student credentials
2. **View Dashboard** to see:
   - Personal timetable based on programme and intake
   - Course schedule
3. **Download Timetable:**
   - Use export buttons to download personal schedule

## Troubleshooting

### Issue: Module not found errors

**Solution:** Ensure virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database errors

**Solution:** Delete db.sqlite3 and run migrations again:
```bash
del db.sqlite3
python manage.py migrate
python manage.py seed_data
```

### Issue: Static files not loading

**Solution:** Run collectstatic:
```bash
python manage.py collectstatic --noinput
```

### Issue: Port already in use

**Solution:** Run on a different port:
```bash
python manage.py runserver 8080
```

## Production Deployment

For production deployment:

1. **Set DEBUG to False** in `settings.py`
2. **Configure ALLOWED_HOSTS** with your domain
3. **Set a strong SECRET_KEY**
4. **Use a production database** (PostgreSQL recommended)
5. **Configure static files** with a web server (nginx/Apache)
6. **Use WSGI server** (Gunicorn/uWSGI)
7. **Enable HTTPS**

## Support

For issues or questions, contact the IT department at Chalimbana University.

## License

© 2025 Chalimbana University. All rights reserved.
