from pathlib import Path
from django.core.management.utils import get_random_secret_key
from django.template.backends import django
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import os

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Helper variables for different environments - debug keys, prod keys and test keys are all supported. API keys are different for each environment
# CAREFUL WITH THIS, setting PROD to true will make the site use production keys and a production database
DEBUG = True
PROD = False
TESTKEYS = True

# Google cloud secret setup. THESE USE ENVIRONMENT VARIABLES, DO NOT LEAK YOUR KEYS
# THESE ARE NOT SET SET IN THE REPOSITORY, SET THEM YOURSELF
# PROD servers are linux based, dev servers are windows based
if PROD:
    # SET YOUR KEY PATH HERE FOR PRODUCTION SERVERS. This is required to access secrets. 
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/django/key.json'
else:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{BASE_DIR}\key.json"


# Method to access secrets. The environment variable for the .json key must be set.
def access_secret(secret_id):
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/gunnigrub/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload

# SENTRY WILL ONLY BE ENABLED IN PRODUCTION. PLEASE DO NOT CLOG UP THE ERROR LOGS WITH TEST ERRORS.
if PROD:
    sentry_sdk.init(
        dsn="", # SET YOUR DSN HERE
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.2,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
    SECRET_KEY = get_random_secret_key()
    # DANGEROUS, make sure you set this to your domain
    ALLOWED_HOSTS = ['35.238.216.71', 'your_url.com', '127.0.0.1']
    sqlpassword = access_secret('sqlpassword')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_name_here',
            'USER': 'db_user_here',
            'PASSWORD': sqlpassword,
            'HOST': 'localhost',
            'PORT': ''
        }
    }

# TEST ONLY USES SQLITE, DO NOT USE FOR PRODUCTION. SQL OR MYSQL IS RECOMMENDED FOR PRODUCTION
else:
    SECRET_KEY = 'django-insecure-au4mra+34)l!cjvmzt9z84u+#x(hn#$v0icw4b!o5@*7fpck(m'
    ALLOWED_HOSTS = []
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

INSTALLED_APPS = [
    'accounts',
    'db',
    'homepage',
    'management',
    'order',
    'processorder',
    'legal',
    'subscription',

    'phonenumber_field',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FoodApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'FoodApp.wsgi.application'

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

AUTH_USER_MODEL = 'accounts.StandardUser'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

LOGIN_URL = '/registration/login'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PHONENUMBER_DEFAULT_REGION = 'US'

# This allows for easy switching between production and development static files, OS file paths are different
if PROD:
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
else:
    STATICFILES_DIRS = [
        BASE_DIR / "static",
        '/var/www/static/',
    ]
STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Stripe API requirements and utility
# SET YOUR DOMAIN HERE
if PROD:
    UTIL_DOMAIN = 'https://FoodAppDomain.com'
else:
    UTIL_DOMAIN = 'http://127.0.0.1:8000'

# API KEYS

# Google Cloud API key: Maps, Places, Captcha

# access_secret(secret_id='Google-API-Key')
RECAPTCHA_SITE_ID = access_secret(secret_id='Recaptcha-Site-ID')

# Stripe API Key (DO NOT LEAK YOU GUYS)
if(TESTKEYS):
    # Stripe will give you different keys for testing and production, make sure you use the right ones. Dummy card info will ONLY work with test keys
    STRIPE_WEBHOOK = "webhook_testing_here"
    STRIPE_API_KEY = access_secret(secret_id='Stripe-Secret-Key-Testing')
    STRIPE_PUBLISHABLE_API_KEY = access_secret(secret_id='Stripe-Publishable-Key-Testing')
    GOOGLE_API_KEY = access_secret(secret_id='Google-Api-Key-Testing')
else:
    STRIPE_WEBHOOK = access_secret(secret_id='stripe-webhook')
    STRIPE_API_KEY = access_secret(secret_id='Stripe-Secret-Key')
    STRIPE_PUBLISHABLE_API_KEY = access_secret(secret_id='Stripe-Publishable-Key')
    GOOGLE_API_KEY = access_secret(secret_id='Google-API-Key')

# Twilio API key
TWILIO_SITE_ID = access_secret(secret_id='twilio-site-id')
TWILIO_AUTH_TOKEN = access_secret(secret_id='twilio-auth-token')
