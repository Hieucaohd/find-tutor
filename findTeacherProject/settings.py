import os
from pathlib import Path
import datetime
import urllib
from django.contrib.auth import get_user_model


def get_user_name_field(payload):
    user_id = payload.get("user_id")
    User = get_user_model()

    user_request = User._default_manager.get(pk=user_id)
    
    return user_request.email


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x6ru6j*)01lp-x+sr$%%afgo+wfbnecjb403xi+vx2tk=gy1)a'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TO_AWS = not DEBUG


ALLOWED_HOSTS = ["*"]   # Allow all hosts!


AUTH_USER_MODEL = 'authentication.User'


# Application definition
INSTALLED_APPS = [
    # django app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # main package
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    'graphene_django',
    'channels', 
    'guardian', 

    # helper package
    'multiselectfield',
    'corsheaders',
    'drf_yasg',

    # my app
    'findTutor',
    'authentication',
    'socialAuth',
    'search',
    'websocket',
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'NON_FIELD_ERROR_KEYS': 'error',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.custom_jwt_auth.simplejwt_token_auth.CustomJWTAuthentication',    # Custom simplejwt for http_only cookie
    )
}


GRAPHENE = {
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
    'GRAPHIQL_HEADER_EDITOR_ENABLED': True,
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
    "authentication.custom_jwt_auth.graphql_token_auth.CustomJSONWebTokenBackend",   # Custom graphql_jwt for http_only cookie
]


TOKEN_PREFIX = 'Bearer'

JWT_COOKIE_CONFIG = {
    "JWT_COOKIE_NAME": "access_token",                                  # Key of access_token
    "JWT_REFRESH_TOKEN_COOKIE_NAME": "refresh_token",                   # Key of refresh_token
    "JWT_COOKIE_SECURE": False,                                          # If True, just allow only https://
    "JWT_COOKIE_HTTP_ONLY": True,                                       # Client and javascript can not get
    "JWT_COOKIE_PATH": "/",                                             # Path of auth token
    "JWT_COOKIE_DOMAIN": None,                                          # 
    "JWT_COOKIE_SAMESITE": None,                                    # It can be 'Lax', 'Strict', None to disable
}

GRAPHQL_JWT = {
    "JWT_ALLOW_ARGUMENT": True,
    "JWT_AUTH_HEADER_PREFIX": TOKEN_PREFIX,
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": (
        lambda payload: get_user_name_field(payload)                    # Identify a user by email
    ),
    **JWT_COOKIE_CONFIG,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'AUTH_HEADER_TYPES': (TOKEN_PREFIX, ),
    **JWT_COOKIE_CONFIG,
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://192.168.29.103:3000",
    "https://timgiasu.vercel.app",
    "https://timgiasu.findtutorapp.website",
]


ROOT_URLCONF = 'findTeacherProject.urls'


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


WSGI_APPLICATION = 'findTeacherProject.wsgi.application'
ASGI_APPLICATION = 'findTeacherProject.asgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'testdb',
        'USER': 'hieucao192',
        'PASSWORD': '192',
        'HOST': 'localhost',
        'PORT': 5432
    }
}


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        }
    }
}


MONGO_URL = "mongodb+srv://hieucao192:" + urllib.parse.quote("Caotrunghieu@192") + "@authenticationtest.6lh8w.mongodb.net/userSearch?retryWrites=true&w=majority"


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'timgiasu.xacnhan@gmail.com'
EMAIL_HOST_PASSWORD = 'Timfgiasuw@2021'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

USE_FIREBASE = True     # User firebase for store image
if USE_FIREBASE:
    MEDIA_URL = ''


# For debug
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('127.0.0.1', 6379)],
            }
        }
    }



