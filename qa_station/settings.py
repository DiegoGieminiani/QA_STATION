"""
Django settings for qa_station project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l*8x1h$3$jx6c@!in^in(t-zxtya*6ni+8fgc4ojrriv9r4w5&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Asegúrate de poner 'jazzmin' al principio para que sobrescriba el admin predeterminado de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #My Apps
    'users',
    'user_documentation',
    'about_us',
    'user_projects',
    'ai_module',

    # Tests
    'functional_tests', 
    'django_extensions',
    'rest_framework'
]


JAZZMIN_SETTINGS = {
    "site_logo": "images/logo.png",  # Asegúrate de tener el logo en la carpeta static
    "site_icon": "images/favicon.png",  # Ícono para el favicon
    "site_title": "Administración QA Station",
    "site_header": "QA Station",
    "site_brand": "QA Station",
    "login_logo": "images/logo.png",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Bienvenido a QA Station",
    "order_with_respect_to": ["users", "user_projects", "ai_module", "functional_tests"],
    "show_sidebar": True,
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-white",
    "accent": "accent-navy",
    "navbar": "navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

JAZZMIN_SETTINGS["show_ui_builder"] = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'qa_station.middleware.LoginRequiredMiddleware'
]

ROOT_URLCONF = 'qa_station.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ], 
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

WSGI_APPLICATION = 'qa_station.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qa_station',  # El nombre de la base de datos que creaste
        'USER': 'root',  # O el nombre del usuario que prefieras
        'PASSWORD': 'QA_Station.,',  # La contraseña que usaste para el usuario de MySQL
        'HOST': 'localhost',  # Normalmente 'localhost' si MySQL está en la misma máquina
        'PORT': '3306',  # El puerto predeterminado de MySQL
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',  # Para soporte completo de caracteres UTF-8
        },
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# URL que utilizará Django para acceder a los archivos estáticos
STATIC_URL = '/static/'

# Si tienes una carpeta de archivos estáticos compartidos:
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# Rutas adicionales de archivos estáticos
#STATICFILES_DIRS = [#
   # BASE_DIR / "static",  # Archivos estáticos generales
    #BASE_DIR / "functional_tests/static",  # Archivos estáticos específicos de functional_tests
#]

# Configuración de archivos multimedia (si aplicas multimedia en el proyecto)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = '/static/'

# Esto permite que Django busque archivos estáticos en las subcarpetas "static" de cada app
#STATICFILES_DIRS = [
#    BASE_DIR / "static",  # Si tienes una carpeta "static" global en el proyecto
#]

# Donde se recopilarán todos los archivos estáticos cuando ejecutes 'collectstatic'
STATIC_ROOT = BASE_DIR / "staticfiles"  # Para producción



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

