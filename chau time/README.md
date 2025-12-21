# Chalimbana University Timetable Scheduling System

A comprehensive web-based timetable scheduling application built with Django for Chalimbana University.

## Features

- **Role-Based Access Control**: Admin, Lecturer, and Student dashboards
- **Auto-Scheduling Algorithm**: Intelligent timetable generation with conflict detection
- **Manual Scheduling**: Fine-tune timetables manually
- **Resource Management**: Manage lecturers, classrooms, programmes, courses, and intakes
- **Export Functionality**: PDF, Excel, and interactive HTML exports
- **Conflict Detection**: Real-time alerts for scheduling conflicts
- **Responsive Design**: Mobile-friendly interface with Chalimbana University branding

## Requirements

- Python 3.11+
- Django 4.2+
- See `requirements.txt` for full dependencies

## Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Load seed data**:
   ```bash
   python manage.py loaddata seed_data.json
   ```

6. **Create a superuser** (optional, if not using seed data):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Open your browser and navigate to `http://127.0.0.1:8000/`

## Default Login Credentials (Seed Data)

### Admin
- Email: `admin@chalimbana.edu.zm`
- Password: `admin123`

### Lecturer
- Email: `lecturer@chalimbana.edu.zm`
- Password: `lecturer123`

### Student (Regular)
- Email: `student@chalimbana.edu.zm`
- Password: `student123`

### Student (Distance)
- Email: `distance@chalimbana.edu.zm`
- Password: `distance123`

## Project Structure

```
chau_time/
├── timetable_project/      # Django project settings
├── timetable/              # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── urls.py             # URL routing
│   ├── forms.py            # Form definitions
│   ├── scheduling.py       # Auto-scheduling algorithm
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, images
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Usage

### Admin Dashboard
- Manage all resources (lecturers, students, classrooms, programmes, courses)
- Generate timetables automatically or manually
- View and resolve conflicts
- Export timetables in multiple formats

### Lecturer Dashboard
- View personal timetable
- Update availability
- View assigned courses
- Receive notifications

### Student Dashboard
- View personal timetable
- Download/export schedule
- View course information
- Receive notifications

## Auto-Scheduling Algorithm

The system uses an intelligent constraint-based scheduling algorithm that:
- Prevents lecturer conflicts
- Prevents classroom conflicts
- Prevents student conflicts
- Considers lecturer availability
- Respects room capacity
- Handles different period types (single/double/multiple)
- Provides alternative suggestions when conflicts occur

## Export Formats

- **PDF**: Professional printable timetables
- **Excel**: Editable spreadsheets for further analysis
- **HTML**: Interactive timetables with clickable lecturer information

## Support

For issues or questions, contact the IT department at Chalimbana University.

## License

© 2025 Chalimbana University. All rights reserved.
