"""
Django settings for energiepanel project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os.path
import os




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v#k7)22c&men&mu8urbcg2w7xt$&c9b18isbnwm1w4969&lbe*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','.localhost', 'energiezelle-88d461a9c8f6.herokuapp.com']

AUTH_USER_MODEL = 'epanel.User'

#Email config
# Hier muss ein SMTP-Mailserver angegeben werden, von dem das Energiepanel die E-Mails zur Bestätigung und Passwortzurücksetzung 
# verschickt.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.your-server.de'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'anmeldung@tsb-energie-daten.de'
EMAIL_HOST_PASSWORD = '*************'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

DEFAULT_FROM_EMAIL = 'anmeldung@tsb-energie-daten.de'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = '/overview'
LOGOUT_REDIRECT_URL = '/logout'

# Application definition

VARS_MODULE_PATH = 'epanel.global_settings'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

INSTALLED_APPS = [
    'constance',
    'constance.backends.database',
    'cookielaw',
    'django_object_actions',
    'csvexport',
    'epanel',
    'crispy_forms',
    'crispy_bootstrap4',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

CONSTANCE_CONFIG = {
    'VBS_WITH_WW': (2400, 'Vollbetriebsstunden mit Warmwasser'),
    'VBS_WITHOUT_WW': (2100, 'Vollbetriebsstunden ohne Warmwasser'),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'energiepanel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'energiepanel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Hier muss die Datenbank (siehe https://docs.djangoproject.com/en/3.2/ref/settings/#databases)
# angegeben werden. Die SQLite-Datenbank sollte ausschließlich zum Testen verwendet werden.
# In der Produktion wird eine MySQL-/MariaDB-Datenbank empfohlen.

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'tsbegd_db1',
    #     'USER': 'tsbegd_1',
    #     'PASSWORD': '***************',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
	# 'OPTIONS': {
    #     	'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    # 	},
    # }
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
   }
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

gettext = lambda x: x

LANGUAGE_CODE = 'de-de'
LANGUAGES = (
    ('de', gettext('German')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = '/usr/home/tsbegd/public_html/static/'

# Windows Test Env
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ( os.path.join('staticfiles'), )


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

