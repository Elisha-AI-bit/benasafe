# Chalimbana University Timetable System - Features

## Overview

A comprehensive web-based timetable scheduling application built with Django, designed specifically for Chalimbana University's academic scheduling needs.

## Core Features

### 1. Role-Based Access Control

#### Administrator
- Full system access and control
- Manage all resources (lecturers, students, courses, classrooms)
- Generate and modify timetables
- View and resolve conflicts
- Export reports and timetables
- Dashboard with system statistics

#### Lecturer
- View personal timetable
- Update availability preferences
- View assigned courses
- Export personal schedule
- Receive notifications

#### Student
- View personal timetable based on programme and intake
- Distinguish between Regular and Distance learning schedules
- Download/export personal schedule (PDF, Excel, HTML)
- View course information
- Receive notifications

### 2. Auto-Scheduling Algorithm

**Intelligent Constraint-Based Scheduling:**
- Automatically generates conflict-free timetables
- Considers multiple constraints:
  - Lecturer availability (day-wise)
  - Classroom capacity and type
  - Course requirements (lab, computers, projector)
  - Student programme and intake
  - Maximum hours per week for lecturers
  - Period types (single, double, triple sessions)

**Scheduling Options:**
- Schedule all programmes at once
- Schedule specific intake
- Schedule individual programme
- Option to clear existing entries or append

**Smart Features:**
- Prefers 2-hour blocks for efficiency
- Respects lunch breaks (12:00-13:00)
- Handles distance learning separately
- Provides detailed success/failure reports

### 3. Conflict Detection & Resolution

**Real-Time Conflict Detection:**
- Lecturer double-booking detection
- Classroom double-booking detection
- Student schedule conflicts
- Automatic conflict logging

**Conflict Management:**
- View all unresolved conflicts
- Detailed conflict descriptions
- Quick access to conflicting entries
- Mark conflicts as resolved
- Alternative time slot suggestions

### 4. Resource Management

#### Lecturers
- Add/Edit/Delete lecturers
- Set initials, contact info, office location
- Define specialization
- Configure weekly availability
- Set maximum teaching hours

#### Students
- Add/Edit/Delete students
- Assign to programmes and intakes
- Distinguish Regular vs Distance learning
- Track year of study
- Store contact information

#### Classrooms
- Add/Edit/Delete venues
- Specify building and room number
- Set capacity
- Define room type (Lecture Hall, Lab, Theatre, Tutorial)
- Mark facilities (projector, computers)
- Set availability status

#### Courses
- Add/Edit/Delete courses
- Assign to programmes and lecturers
- Set year of study and semester
- Define credit hours
- Specify hours per week
- Set room preferences
- Mark special requirements (lab, computers)

#### Programmes
- Add/Edit programmes
- Assign to schools/faculties
- Set duration
- Track enrolled students and courses

#### Intakes
- Add/Edit intake periods
- Set start and end dates
- Mark as active/inactive
- Track enrolled students

### 5. Timetable Display

**Grid View:**
- Weekly timetable grid
- Days (Monday-Friday, optional Saturday/Sunday)
- Time slots (08:00-18:00)
- Color-coded entries
- Lunch break indicators

**Filtering:**
- Filter by programme
- Filter by intake
- Filter by lecturer
- Filter by classroom

**Information Display:**
- Course code and name
- Lecturer initials and name
- Classroom location
- Session duration
- Programme and intake

### 6. Export Functionality

#### PDF Export
- Professional printable format
- University branding (red, blue, white)
- Weekly grid layout
- Course details
- Suitable for printing and distribution

#### Excel Export
- Editable spreadsheet format
- Multiple sheets (timetable, resources)
- Formatted cells with borders
- Easy data manipulation
- Suitable for further analysis

#### Interactive HTML Export
- Standalone HTML file
- Clickable lecturer names
- Modal popups with lecturer information
  - Contact details (email, phone)
  - Office location
  - Assigned courses
- Print-friendly
- Works offline
- Responsive design

#### Resource Allocation Report
- Excel format
- Lecturer utilization
- Classroom usage statistics
- Programme overview
- Student enrollment data

### 7. Manual Scheduling

**Flexible Entry Creation:**
- Add individual timetable entries
- Select course, lecturer, classroom
- Choose programme and intake
- Set day and time
- Specify session type
- Mark for distance learning

**Entry Management:**
- Edit existing entries
- Delete entries
- Automatic conflict checking on save

### 8. Dashboard Features

#### Admin Dashboard
- Total counts (lecturers, students, courses, classrooms)
- Active programmes and intakes
- Timetable entries count
- Unresolved conflicts alert
- Quick action buttons
- Recent conflicts list

#### Lecturer Dashboard
- Personal information display
- Assigned courses list
- Personal timetable
- Export options
- Availability update link

#### Student Dashboard
- Student information
- Programme and intake details
- Personal timetable
- Export options
- Course schedule

### 9. User Interface

**Design:**
- Chalimbana University branding
- Color scheme: Red (#C41E3A), Blue (#003DA5), White
- Clean, modern interface
- Intuitive navigation
- Responsive design

**Responsive Layout:**
- Mobile-friendly
- Tablet-optimized
- Desktop-enhanced
- Touch-friendly controls
- Adaptive grids

**User Experience:**
- Clear visual hierarchy
- Consistent styling
- Helpful tooltips
- Success/error messages
- Loading indicators
- Confirmation dialogs

### 10. Notifications System

**User Notifications:**
- Timetable updates
- Conflict alerts
- Schedule changes
- System announcements
- Mark as read functionality

### 11. Security Features

**Authentication:**
- Email-based login
- Secure password hashing
- Session management
- Role-based permissions

**Authorization:**
- View restrictions by role
- Action restrictions by role
- Protected admin functions
- CSRF protection

### 12. Data Validation

**Form Validation:**
- Required field checking
- Email format validation
- Date range validation
- Capacity constraints
- Unique constraints (student ID, course code)

**Business Logic Validation:**
- Lecturer availability checking
- Classroom capacity verification
- Time slot overlap detection
- Programme-course compatibility

## Technical Specifications

### Backend
- **Framework:** Django 4.2+
- **Language:** Python 3.11+
- **Database:** SQLite (development), PostgreSQL-ready
- **Authentication:** Django built-in auth system

### Frontend
- **HTML5** with Django templates
- **CSS3** with custom styling
- **Vanilla JavaScript** for interactivity
- **Responsive design** without heavy frameworks

### Libraries
- **ReportLab:** PDF generation
- **OpenPyXL:** Excel file generation
- **Pillow:** Image processing
- **python-dateutil:** Date utilities

### Architecture
- **MVC Pattern** (Model-View-Controller)
- **RESTful URL structure**
- **Modular design**
- **Separation of concerns**

## Performance

- Efficient database queries with `select_related` and `prefetch_related`
- Bulk operations for large datasets
- Optimized scheduling algorithm
- Minimal external dependencies
- Fast page load times

## Scalability

- Supports multiple schools/faculties
- Handles hundreds of courses
- Manages thousands of students
- Processes complex scheduling scenarios
- Extensible architecture

## Future Enhancement Possibilities

- Email notifications
- SMS alerts
- Mobile app
- Calendar integration (iCal, Google Calendar)
- Room booking system
- Attendance tracking
- Grade management
- Online exam scheduling
- Multi-language support
- API for third-party integrations
