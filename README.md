# BeneSafe - Digital Asset and Beneficiary Management System

BeneSafe is a comprehensive digital asset and beneficiary management system built with Django that helps individuals and families record, store, and verify their personal, financial, and asset data in a structured way.

## Features

### Core Features
- **Secure data storage** with encrypted file paths
- **User authentication** with email verification and password reset
- **Role-based access control** (User, Verifier, Admin)
- **Bouquet-based subscription system** (Blue, Red, Gold)
- **File/document uploads** (PDF, images, CSV, Word, Excel)
- **Document verification workflows**
- **Export capabilities** (PDF, CSV, Excel, ZIP)

### Asset Management
- Bank Accounts (with branch and account details)
- Insurance & Social Security (policies and coverage)
- Village Banking Groups (Chilimba management)
- Houses/Land (property details with GPS coordinates)
- Motor Vehicles (registration, chassis, engine details)
- Projects (tracking progress and contacts)
- General Assets (serial numbers, warranties)
- Treasury Bonds (investment tracking)
- IP Rights (patents, trademarks, copyrights)

### Additional Modules
- **Liability Management** (loans, advances, refunds)
- **Business/Partnership Management** (PACRA entities)
- **Professional Services Directory** (trusted contacts)
- **Beneficiaries Management** (emergency contacts)
- **Document Verification** (Corporate & Legal workflows)
- **Subscription & Billing** (payment processing)
- **Reward Tracking** (loyalty program for Gold members)

## Technology Stack

- **Backend**: Django 5+, Django REST Framework
- **Database**: PostgreSQL (production), SQLite (development)
- **Frontend**: Bootstrap 5, Chart.js, custom CSS/JS
- **File Storage**: Django Storages (local/cloud options)
- **PDF Generation**: ReportLab, WeasyPrint
- **Excel Export**: OpenPyXL
- **Authentication**: Django Auth with email verification

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd benesafe
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Admin: http://localhost:8000/admin/
   - Main site: http://localhost:8000/

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Settings
The main configuration is in `bene_safe/settings.py`:

- **BOUQUET_PRICES**: Subscription pricing
- **FILE_UPLOAD_MAX_MEMORY_SIZE**: File upload limits
- **REST_FRAMEWORK**: API throttling and authentication

## Project Structure

```
bene_safe/
├── accounts/           # Authentication & user profiles
├── assets/            # Asset management system
├── liabilities/       # Debt and loan tracking
├── businesses/        # Business partnerships
├── professionals/     # Service provider directory
├── beneficiaries/     # Emergency contacts
├── verification/      # Document verification workflows
├── billing/          # Subscriptions & payments
├── documents/        # File upload/download management
├── core/             # Dashboard & main views
├── media/            # User uploaded files
├── static/           # CSS, JS, images
└── templates/        # HTML templates
```

## API Endpoints

The system provides REST API endpoints for:
- User authentication and profiles
- Asset CRUD operations
- Document upload/download
- Verification workflows
- Billing and subscriptions

Access API documentation at: http://localhost:8000/api/

## User Roles

### User
- Register and manage personal data
- Upload and manage assets and documents
- Export personal data in various formats
- Subscribe to bouquet plans

### Verifier (Corporate & Legal)
- Review and verify submitted documents
- Approve or reject asset documentation
- Access verification dashboard
- Generate verification reports

### Admin
- Manage all users and subscriptions
- Configure system settings
- Access admin dashboard
- Handle billing and payments

## Subscription Plans

### Blue Plan (K70/month)
- Basic asset management
- Document storage up to 100MB
- Standard export options

### Red Plan (K120/month)
- All Blue features
- Advanced verification workflows
- Priority support
- Extended document storage (500MB)

### Gold Plan (K200/month)
- All Red features
- Loyalty rewards program
- Premium export options
- Advanced analytics dashboard

## Security Features

- **CSRF Protection**: All forms protected
- **File Upload Security**: Type and size validation
- **Role-based Permissions**: Access control middleware
- **API Throttling**: Rate limiting for API endpoints
- **Secure Headers**: Security middleware enabled

## Deployment

### Docker Setup
```bash
docker build -t benesafe .
docker run -p 8000:8000 benesafe
```

### Production Deployment
1. Set `DEBUG=False` in settings
2. Configure production database
3. Set up static file serving
4. Configure email backend
5. Set up SSL/TLS certificates

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Code Style
Follow PEP 8 and Django best practices. Use Black for code formatting.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Email: support@benesafe.com
- Documentation: [Link to docs]
- Issue Tracker: [Link to issues]

## Roadmap

### Version 2.0
- Mobile app integration
- AI document verification
- OCR-based ID recognition
- Payment gateway integration
- Multi-language support

### Version 3.0
- Blockchain integration for document verification
- Advanced analytics and reporting
- API marketplace for third-party integrations
- Social features for family asset sharing
