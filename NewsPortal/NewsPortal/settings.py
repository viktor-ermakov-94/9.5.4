"""
Django settings for NewsPortal project.

Generated by 'django-admin startproject' using Django 3.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o05f1yuuqfpeln3*2onu27=zf9_$w@su=((&xgu@c8s86mo89*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# подключаем фронтенд
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # надо указать не имя нашего приложения, а его конфиг, чтобы всё заработало
    'appointment.apps.AppointmentConfig',

    'NewsPaper.apps.NewspaperConfig',
    
    'django.contrib.sites',
    'django.contrib.flatpages',

    # для allauth добавляем следующие приложения
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # добавляем провайдеров, которые необходимо подключить (например, Google):
    'allauth.socialaccount.providers.google',

    'django_filters',

    #'NewsPaper',
    #'appointment',

]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'NewsPortal.urls'

TEMPLATES = [
    {
        # указываем, что в качестве templates используем шаблоны Django
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # указываем путь, по которому нужно искать все шаблоны html
        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        # нужно ли искать Django наши шаблоны по пути DIRS?
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # allauth
                'django.template.context_processors.request'

            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# добавим настройки о том, что поле email является обязательным и уникальным
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
# поле username необязательно
ACCOUNT_USERNAME_REQUIRED = False
# укажем, что аутентификация будет происходить посредством электронной почты
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# укажем, что верификация почты отсутствует (подтверждение аккаунта через письмо на почту)
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# тема письма для подтверждения регистрации
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Skillfactory sends it's regards. "
# если пользователь вышел, его перенаправит на страницу:
LOGOUT_REDIRECT_URL = '/accounts/login/'
# при успешной авторизации, пользователя перенаправит на домашнюю страницу
LOGIN_REDIRECT_URL = 'home'
# при неуспешной авторизации, пользователя должно перенаправить на страницу регистрации
LOGIN_URL = '/accounts/signup/'

WSGI_APPLICATION = 'NewsPortal.wsgi.application'

# чтобы allauth выполнил именно эту форму при регистрации пользователя,
# а не ту, что по умолчанию, напишем:
ACCOUNT_FORMS = {'signup': 'NewsPaper.forms.BasicSignupForm'}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '11904522129-bc1puonklcf5h87di7j56n8qma2fuh25.apps.googleusercontent.com',
            'secret': '1XGC2Q8fpW2Dyvh22gwWhtsC',
            'key': ''
        }
    }
}

EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'FPW-13'  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = 'dV8-Zxg-ebQ-wZ3'  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно

# указываем ПОЛНУЮ почту, с которой будут отправляться письма
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER + '@yandex.ru'

ADMINS = [
    ('Bulat', 'bulat_man@mail.ru'),
    # список всех админов в формате ('имя', 'их почта')
]

# для отправки писем менеджерам через функцию mail_managers
MANAGERS = [
    ('Bulat', 'FPW-13@yandex.ru'),
]

SERVER_EMAIL = 'FPW-13@yandex.ru'  # это будет у нас вместо аргумента FROM в массовой рассылке

# True позволит избежать дополнительных действий и активирует аккаунт сразу, как только мы перейдем по ссылке
# False попросит подтвердить ещё раз на сайте после прохождения по ссылке
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# количество дней, в течение которых будет доступна ссылка на подтверждение регистрации
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
