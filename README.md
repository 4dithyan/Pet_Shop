# Premium Pet Shop Management System - Setup Guide

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10 or higher
- XAMPP (for MySQL)
- Web browser (Chrome/Firefox recommended)

---

## 📋 Step-by-Step Installation

### 1. Set Up XAMPP and MySQL

1. **Start XAMPP Control Panel**
   - Start **Apache** and **MySQL** services

2. **Create Database**
   - Open browser: `http://localhost/phpmyadmin`
   - Click "New" in left sidebar
   - Database name: `petshop_db`
   - Collation: `utf8mb4_unicode_ci`
   - Click "Create"

3. **Import Schema (Optional)**
   ```bash
   # From phpMyAdmin, select petshop_db, then:
   # Click "Import" > Choose File > Select database_schema.sql
   # Or let Django create tables automatically with migrations
   ```

---

### 2. Install Python Dependencies

```bash
# Navigate to project directory
cd d:\Theres\Anandhu\Petstore

# Install required packages
pip install -r requirements.txt
```

**Required packages:**
- Django==5.0.1
- mysqlclient==2.2.1
- Pillow==10.2.0
- django-crispy-forms==2.1
- crispy-bootstrap5==2.0.0

**If mysqlclient fails on Windows:**
```bash
# Install wheel first
pip install wheel

# Then try again
pip install mysqlclient
```

---

### 3. Run Database Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to create tables
python manage.py migrate
```

---

### 4. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create admin credentials:
- Username: `admin` (or your choice)
- Email: `admin@petshop.com`
- Password: (choose a secure password)

---

### 5. Create Media Directories

Django will create these automatically, but you can create manually:

```bash
mkdir media
mkdir media\pets
mkdir media\products
mkdir media\profile_pics
```

---

### 6. Run the Development Server

```bash
python manage.py runserver
```

**Access the application:**
- Homepage: `http://localhost:8000`
- Admin Panel: `http://localhost:8000/admin`
- Dashboard: `http://localhost:8000/dashboard`

---

## 🎨 Frontend Libraries (CDN - Already Configured)

The templates use these libraries via CDN:
- **Bootstrap 5.3** - UI Framework
- **Swiper.js 11** - Hero Slideshow
- **GSAP 3** + ScrollTrigger - Animations
- **AOS 2** - Scroll Animations
- **Chart.js 4** - Dashboard Charts
- **Font Awesome 6** - Icons

No additional installation needed!

---

## 📁 Project Structure

```
Petstore/
├── petshop/                 # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # User authentication
├── pets/                    # Pet management
├── products/                # Product & inventory
├── cart/                    # Shopping cart
├── orders/                  # Order processing
├── appointments/            # Appointment booking
├── reviews/                 # Review system
├── dashboard/               # Admin dashboard
├── static/                  # Static files
│   ├── css/
│   │   ├── main.css        # Global styles
│   │   ├── home.css        # Homepage styles
│   │   ├── dashboard.css   # Dashboard styles
│   │   └── animations.css  # Animation effects
│   └── js/
│       ├── main.js         # Global JavaScript
│       ├── home.js         # Homepage animations
│       ├── dashboard.js    # Dashboard charts
│       └── cart.js         # Cart operations
├── templates/               # HTML templates
├── media/                   # User uploads
├── manage.py
├── requirements.txt
└── database_schema.sql     # MySQL schema
```

---

## 🔧 Configuration

### Database Settings (petshop/settings.py)

Already configured for XAMPP:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'petshop_db',
        'USER': 'root',
        'PASSWORD': '',  # Empty for XAMPP
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Static Files

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 🌟 Features Implemented

### ✅ Backend Features
- ✅ Custom User model with role-based access (Admin, Customer, Staff)
- ✅ Pet management (CRUD with images, categories, search)
- ✅ Product management with inventory tracking
- ✅ Session-based shopping cart
- ✅ Order processing with automatic stock reduction
- ✅ Appointment booking system
- ✅ Review & rating system
- ✅ Admin dashboard with Chart.js analytics

### ✅ Frontend Features
- ✅ Modern, premium design system
- ✅ Responsive grid layout
- ✅ Separate CSS files (main, home, dashboard, animations)
- ✅ Separate JavaScript files (main, home, dashboard, cart)
- ✅ Ready for Swiper.js hero slideshow
- ✅ GSAP & AOS animation setup
- ✅ Chart.js dashboard integration
- ✅ Custom animations and micro-interactions

---

## 🎯 Next Steps

### To Complete the System:

1. **Create HTML Templates**
   - [x] `templates/base.html` - Main layout
   - [x] `templates/home.html` - Homepage with all sections
   - [x] `templates/navbar.html` - Navigation component
   - [x] Template files for each app (accounts, pets, products, etc.)

2. **Add Sample Data**
   - Add pet images to `media/pets/`
   - Add product images to `media/products/`
   - Create sample pets and products via admin panel

3. **Test All Features**
   - User registration and login
   - Pet browsing and filtering
   - Add to cart and checkout
   - Appointment booking
   - Admin dashboard functionality

---

## 🐛 Troubleshooting

### Common Issues:

**1. mysqlclient installation fails**
```bash
# Solution: Install Visual C++ redistributables
# Or use PyMySQL as alternative
pip install pymysql
# Add to settings.py:
import pymysql
pymysql.install_as_MySQLdb()
```

**2. Database connection error**
- Ensure XAMPP MySQL is running
- Check database name in settings.py
- Verify root password (default is empty)

**3. Static files not loading**
```bash
python manage.py collectstatic
```

**4. Module not found errors**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📊 Admin Dashboard Access

1. Login to admin: `http://localhost:8000/admin`
2. Use superuser credentials
3. Add sample data:
   - Categories (Dogs, Cats, Birds, Fish)
   - Pets with images
   - Products with stock quantities
   - Product categories

---

## 🎨 Design System

### Color Palette
- Primary: `#2EC4B6` (Teal)
- Secondary: `#FF6B6B` (Coral)
- Dark: `#0F172A` (Navy)
- Background: `#F9FAFB` (Off-white)
- Accent: `#FFD166` (Gold)

### Typography
- Font: Poppins (Google Fonts)
- Headings: 700-800 weight
- Body: 400-600 weight

### Border Radius
- Small: 8px
- Medium: 12px
- Large: 16px
- XL: 24px

---

## 📱 Responsive Breakpoints

- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: <768px

---

## 🔐 Security Features

- ✅ CSRF protection on all forms
- ✅ Password hashing (Django default)
- ✅ Login required decorators
- ✅ Staff-only access for admin features
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection

---

## 📖 Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap 5: https://getbootstrap.com/
- Swiper.js: https://swiperjs.com/
- GSAP: https://greensock.com/gsap/
- Chart.js: https://www.chartjs.org/

---

## 💡 Tips

1. **Development Mode**: Keep `DEBUG = True` in settings.py during development
2. **Production**: Change `DEBUG = False` and set proper `ALLOWED_HOSTS`
3. **Secret Key**: Generate new secret key for production
4. **Database Backup**: Regularly backup your MySQL database
5. **Media Files**: Keep backups of uploaded images

---

## 🎉 You're Ready!

The backend is fully functional with:
- 8 Django apps
- Complete database schema
- Separate CSS/JavaScript files
- Professional code structure
- Production-ready architecture

Happy coding! 🐾
