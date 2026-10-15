import os
from pathlib import Path
import dj_database_url
from django.templatetags.static import static

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ithihas-photography-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # Unfold Admin Theme (must come before django.contrib.admin)
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',

    # Custom App
    'portfolio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ithihas_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ithihas_project.wsgi.application'


# Database

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# Static and Media Files Configuration

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django Unfold Admin Theme Configuration
# Django Unfold Admin Theme Configuration
UNFOLD = {
    "SITE_TITLE": "ITHIHAS Photography Admin",
    "SITE_HEADER": "ITHIHAS",
    "SITE_URL": "/",
    "SITE_FAVICON": lambda request: "https://res.cloudinary.com/lflhno7m/image/upload/v1792039015/Ithihas1.1_3x.png",
    # Logo displayed on the login page above the welcome title
    "SITE_LOGO": {
        "light": lambda request: "https://res.cloudinary.com/lflhno7m/image/upload/v1792039015/Ithihas1.1_3x.png",
        "dark": lambda request: "https://res.cloudinary.com/lflhno7m/image/upload/v1791996847/static/images/ithihas_logo.17aa0464ebee.png",
    },
    # Small icon displayed in navigation top bar
    "SITE_ICON": {
        "light": lambda request: "https://res.cloudinary.com/lflhno7m/image/upload/v1792039015/Ithihas1.1_3x.png",
        "dark": lambda request: "https://res.cloudinary.com/lflhno7m/image/upload/v1791996847/static/images/ithihas_logo.17aa0464ebee.png",
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
    },
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "17 24 39",
            "default-dark": "243 244 246",
            "muted-light": "156 163 175",
            "muted-dark": "107 114 128",
        },
        "primary": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
    },
}

# Cloudinary Media Storage Configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'lflhno7m',
    'API_KEY': '464393156323861',
    'API_SECRET': 'zAmV49HViWxrFSZtUc64wnnNoRY',
    'SECURE': True,  # Force HTTPS URLs
}

# Storage Backends & Legacy Compatibility Fallback
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# Brevo (Sendinblue) SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('BREVO_SMTP_USER')
EMAIL_HOST_PASSWORD = os.getenv('BREVO_SMTP_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'ithihasbyvd@gmail.com')

