"""
Django settings for user_auth_project project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from django.contrib.messages import constants as messages
from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-&(ff0xhw013b)68z3d2c19b6)20@^3!xioy2z!y!v(8+v=i^io"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['irokane.pythonanywhere.com']


# Application definition
INSTALLED_APPS = [
    "accounts",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "user_auth_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "user_auth_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# settings.py


MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

SESSION_COOKIE_AGE = 300
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # ブラウザを閉じたときにログアウト
SESSION_SAVE_EVERY_REQUEST = True
LOGIN_REDIRECT_URL = '/accounts/home/'


# 認証バックエンドの設定（必要に応じて）
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'accounts.backends.EmailBackend',  # カスタムバックエンドを使用する場合
]



# カスタムユーザーモデルの設定
AUTH_USER_MODEL = 'accounts.CustomUser'



TWITTER_API_KEY = 'あなたのAPIキー'
TWITTER_API_SECRET_KEY = 'あなたのAPIシークレットキー'
TWITTER_ACCESS_TOKEN = 'あなたのアクセス・トークン'
TWITTER_ACCESS_TOKEN_SECRET = 'あなたのアクセス・トークン・シークレット'

# AXES_FAILURE_LIMIT = 5  # 試行回数の制限
# AXES_COOLOFF_TIME = timedelta(minutes=1)  # ロックアウトの時間
# AXES_LOCKOUT_TEMPLATE = 'accounts/lockout.html'  # ロックアウト時のテンプレート
# AXES_RESET_ON_SUCCESS = True  # 成功したログインでカウンターリセット
# AXES_USERNAME_FORM_FIELD = 'email'
# AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']
# # IP アドレスの取得に関する設定
# AXES_IPWARE_META_PRECEDENCE_ORDER = ('REMOTE_ADDR',)  # IP アドレスの順序を設定
# AXES_CLIENT_IP_CALLABLE = None  # IP を取得する関数

# # ユーザーエージェントに関する設定
# AXES_USE_USER_AGENT = True

# # IP とユーザーエージェントの設定を無効にしてテストする
# #（ユーザー名だけでロックアウトを確認するため）
# AXES_LOCKOUT_PARAMETERS = ['username'] 



EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
PASSWORD_RESET_TIMEOUT = 300  # 5分

LOGIN_URL = "/accounts/login"
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
