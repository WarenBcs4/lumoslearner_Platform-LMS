# Lumos Learning

![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive, production-ready Learning Management System (LMS) built with Django, featuring modern payment integration, content access control, and a beautiful responsive UI.

## 🌟 Key Features

### For Students
- ✅ **Free Registration** - Easy sign-up process
- 📚 **Free Content Preview** - Access first 10 pages of PDFs for free
- 🎥 **Free First Episode** - Watch first video episode of any course for free
- 💳 **Multiple Payment Options** - PayPal (global) and InterSend (Kenya local)
- 📅 **Personal Schedule Management** - Plan and track your learning schedule
- 📊 **Progress Tracking** - Track your learning progress across all materials
- 🏆 **Certificates** - Earn certificates upon course completion
- ⭐ **Course Reviews** - Rate and review courses

### For Teachers/Content Creators
- 📤 **Content Upload** - Upload PDFs, eBooks, and videos
- 💰 **Monetization** - Set prices for premium content
- 📈 **Analytics** - Track course performance and student engagement
- 👥 **Student Management** - View enrolled students and their progress

### For Administrators
- 🎛️ **Full Control Panel** - Comprehensive Django admin interface
- 👤 **User Management** - Manage users, roles, and permissions
- 📊 **Payment Tracking** - Monitor all transactions and refunds
- ✅ **Content Moderation** - Approve/reject reviews and content
- 📧 **Email Notifications** - Automated emails for enrollments, payments

## 💰 Pricing Structure

- **PDF Access**: $2.00 one-time payment (after 10 free pages)
- **Video Episodes**: $3.00 one-time payment (first episode always free)
- **Full Courses**: Custom pricing set by instructors

## 🛠️ Technology Stack

- **Backend**: Django 4.2 (Python 3.11)
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Task Queue**: Celery
- **Web Server**: Gunicorn + Nginx
- **Payment**: PayPal SDK, InterSend API
- **Storage**: Local + AWS S3 (optional)
- **Authentication**: Django Allauth
- **API**: Django REST Framework
- **Security**: CSP, Rate Limiting, HTTPS

## 📋 Prerequisites

- Docker Desktop installed
- Python 3.11+ (for local development)
- PostgreSQL 15+ (if not using Docker)
- Redis 7+ (if not using Docker)

## 🚀 Quick Start with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/lumos-learning.git
cd lumos-learning
```

### 2. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` and configure your settings:

```env
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

DATABASE_URL=postgresql://lumos_user:secure_password@db:5432/lumos_db

PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Start with Docker Desktop

```bash
# Build and start all services
docker-compose up -d --build

# Create database tables
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### 4. Access the Application

- **Frontend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/api/docs

## 🔧 Local Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb lumos_db

# Run migrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
# Start Redis (in another terminal)
redis-server

# Start Celery worker (in another terminal)
celery -A lumos worker -l info

# Start Django development server
python manage.py runserver
```

## 📁 Project Structure

```
lumos_learning/
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Docker image configuration
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env.example               # Environment variables template
├── manage.py                   # Django management script
│
├── lumos/                      # Main project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI application
│
├── core/                       # Core functionality
│   ├── models.py              # User models
│   ├── views.py               # Core views
│   ├── admin.py               # Admin configuration
│   ├── middleware.py          # Custom middleware
│   └── context_processors.py # Template context
│
├── courses/                    # Course management
│   ├── models.py              # Course, Material, Enrollment models
│   ├── views.py               # Course views & PDF/Video handling
│   ├── forms.py               # Course forms
│   └── admin.py               # Course admin
│
├── payments/                   # Payment processing
│   ├── models.py              # Payment models
│   ├── views.py               # Payment views
│   ├── paypal_integration.py # PayPal SDK integration
│   └── admin.py               # Payment admin
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── home.html              # Landing page
│   ├── dashboard.html         # User dashboard
│   ├── courses/               # Course templates
│   │   ├── course_list.html
│   │   ├── course_detail.html
│   │   ├── pdf_viewer.html
│   │   └── video_player.html
│   └── payments/              # Payment templates
│       ├── checkout.html
│       └── payment_success.html
│
├── static/                     # Static files
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript
│   └── images/                # Images
│
└── media/                      # User uploads
    ├── pdfs/                  # PDF files
    ├── videos/                # Video files
    ├── ebooks/                # eBook files
    └── profiles/              # Profile pictures
```

## 🔐 Security Features

- **HTTPS Enforcement** - SSL/TLS encryption in production
- **CSRF Protection** - Cross-Site Request Forgery protection
- **XSS Prevention** - Content Security Policy headers
- **SQL Injection Protection** - Django ORM parameterized queries
- **Rate Limiting** - Prevent brute force attacks
- **Password Hashing** - PBKDF2 with SHA256
- **Session Security** - Secure session cookies
- **File Upload Validation** - Strict file type checking

## 👥 User Roles

### 1. Student
- Browse and enroll in courses
- Access free content
- Purchase premium content
- Track learning progress
- Manage schedule
- Write reviews

### 2. Teacher/Content Creator
- Upload course materials
- Set pricing
- View analytics
- Manage enrolled students

### 3. Content Manager
- Moderate content
- Approve/reject uploads
- Manage categories

### 4. Administrator
- Full system access
- User management
- Payment management
- System configuration

## 💳 Payment Integration

### PayPal Setup

1. Create PayPal Developer Account: https://developer.paypal.com
2. Create REST API App
3. Get Client ID and Secret
4. Add to `.env` file

```env
PAYPAL_MODE=sandbox  # or 'live' for production
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
```

### InterSend Setup (Kenya)

1. Register at InterSend
2. Get API credentials
3. Configure webhook URL
4. Add credentials to `.env`

## 📧 Email Configuration

Configure email settings in `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

For Gmail, use App Password: https://support.google.com/accounts/answer/185833

## 🌐 Deployment

### Docker Deployment (Recommended)

```bash
# On your server
git clone https://github.com/yourusername/lumos-learning.git
cd lumos-learning

# Configure environment
cp .env.example .env
nano .env  # Edit with production values

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## 📊 Admin Dashboard Access

1. Navigate to `/admin`
2. Login with superuser credentials
3. Manage:
   - Users and roles
   - Courses and materials
   - Payments and transactions
   - Reviews and ratings
   - Site settings

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test courses

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: See `/docs` folder
- **Issues**: Create GitHub issue
- **Email**: support@lumoslearning.com
- **Community**: Join our Discord server

## 🎯 Roadmap

- [ ] Mobile apps (iOS/Android)
- [ ] Live streaming classes
- [ ] AI-powered recommendations
- [ ] Gamification features
- [ ] Multi-language support
- [ ] WhatsApp integration
- [ ] Offline mode
- [ ] Social learning features

## 👏 Acknowledgments

- Django Framework
- PostgreSQL Database
- PayPal SDK
- Bootstrap 5
- Font Awesome Icons

---

**Built with ❤️ by Waren (BCS), Damien (BCS), Stanley (SOEN)**