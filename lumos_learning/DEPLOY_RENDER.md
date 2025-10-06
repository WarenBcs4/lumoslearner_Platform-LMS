# Deploy Lumos Learning to Render

## Quick Deployment Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/lumos-learning.git
git push -u origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and create:
   - Web Service (Django app)
   - PostgreSQL Database
   - Redis Instance

### 3. Set Environment Variables
In Render dashboard, add these environment variables:

**Required:**
- `PAYPAL_CLIENT_ID` - Your PayPal client ID
- `PAYPAL_CLIENT_SECRET` - Your PayPal client secret
- `EMAIL_HOST_USER` - Your email (e.g., Gmail)
- `EMAIL_HOST_PASSWORD` - Your email app password

**Optional:**
- `PAYPAL_MODE` - `sandbox` or `live` (default: sandbox)
- `EMAIL_HOST` - SMTP host (default: smtp.gmail.com)

### 4. Create Superuser
After deployment, run in Render shell:
```bash
python manage.py createsuperuser
```

### 5. Access Your App
- **Frontend:** https://your-app-name.onrender.com
- **Admin:** https://your-app-name.onrender.com/admin

## Manual Deployment (Alternative)

### 1. Create Web Service
- Service Type: Web Service
- Build Command: `./build.sh`
- Start Command: `gunicorn lumos.wsgi:application`
- Environment: Python 3.11

### 2. Create Database
- Database Type: PostgreSQL
- Name: lumos-db

### 3. Create Redis
- Service Type: Redis
- Name: lumos-redis

### 4. Connect Services
Link database and Redis to your web service in environment variables.

## Post-Deployment

### Create Sample Data
```bash
# In Render shell
python manage.py shell
```

```python
from core.models import User
from courses.models import Category, Course

# Create categories
Category.objects.create(name="Programming", slug="programming")
Category.objects.create(name="Design", slug="design")

# Create teacher
teacher = User.objects.create_user(
    username='teacher1',
    email='teacher@example.com',
    password='password123',
    role='teacher',
    is_teacher_approved=True
)
```

## Troubleshooting

### Common Issues:
1. **Build fails:** Check Python version in `render.yaml`
2. **Database connection:** Verify DATABASE_URL is set
3. **Static files:** Ensure WhiteNoise is configured
4. **Email not working:** Check Gmail app password

### Logs:
View logs in Render dashboard under "Logs" tab.

## Production Checklist
- [ ] Set DEBUG=False
- [ ] Configure custom domain
- [ ] Set up SSL certificate
- [ ] Configure email settings
- [ ] Set PayPal to live mode
- [ ] Set up monitoring
- [ ] Configure backups