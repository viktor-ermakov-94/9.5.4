from pathlib import Path
import os

# localization
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o05f1yuuqfpeln3*2onu27=zf9_$w@su=((&xgu@c8s86mo89*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

SITE_ID = 1

# подключаем фронтенд
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # добавляем приложение для запуска периодических задач
    'django_apscheduler',

    'django_celery_beat',
    'django_celery_results',

    # 'debug_toolbar',

    # надо указать не имя нашего приложения, а его конфиг, чтобы всё заработало
    'appointment.apps.AppointmentConfig',

    # 'NewsPaper.apps.NewspaperConfig',

    'django.contrib.sites',
    'django.contrib.flatpages',

    # для allauth добавляем следующие приложения
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # добавляем провайдеров, которые необходимо подключить (например, Google):
    'allauth.socialaccount.providers.google',

    'django_filters',

    'NewsPaper',
    # 'appointment',
    'D14Locale'

]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
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

INTERNAL_IPS = [
    '127.0.0.1',
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

TIME_ZONE = 'UTC'

USE_I18N = True # включена интернационализация

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

# Указываем формат даты для scheduler
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# Время на выполнение задачи (задача снимается, если не успеет выполниться)
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # seconds

# Настройки Celery

# URL брокера сообщений (Redis). По умолчанию он находится на порту 6379
CELERY_BROKER_URL = 'redis://localhost:6379'

# хранилище результатов выполнения задач
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# допустимый формат данных
CELERY_ACCEPT_CONTENT = ['application/json']

# метод сериализации задач
CELERY_TASK_SERIALIZER = 'json'

# метод сериализации результатов
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# подключаем таски, чтоб Селери их нашёл
CELERY_IMPORTS = (
    'NewsPaper.newsletter.tasks',
)

# кэширование
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}


#  логгирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'style': '{',

    # filter
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },

        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },

    # formatter
    'formatters': {
        # задание 13.4 пункт 1
        'format_debug': {
            'format': '{asctime} {levelname} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'format_warning': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'format_error_critical': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'format_general': {
            'format': '{asctime} {levelname} {module} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },

        # задание 13.4 п.4
        'format_security': {
            'format': '{asctime} {levelname} {module} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },

        # задание 13.4 п.5
        'format_errors': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        }
    },

    # handler
    'handlers': {
        # задание 13.4 п.1
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'], # false - отключено
            'class': 'logging.StreamHandler',
            'formatter': 'format_debug',
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_warning'
        },
        'console_errors': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_error_critical'
        },

        # задание 13.4 п.3
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'format_error_critical'
        },

        # задание 13.4 п.2
        'general_log': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'format_general'
        },

        # задание 13.4 п.4
        'security_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'format_security'
        },

        # задание 13.4 п.5
        'mail_admins': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },

    },

    # LOGGER
    # задание 13.4 п.1,
    # задание 13.4 п.2 - добавлено значение в handlers = 'general_log'
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_errors', 'general_log'],  # choosing handler names which where specified above
            'level': 'DEBUG',  # choosing the same or above level than it's specified in handlers. Otherwise, we won't be able to handle some of them.
        },


        # задание 13.4 п.3
        # задание 13.4 п.5 - добавлено
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
        },
        'django.server': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
        },
        'django.template': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
        },
        'django.db_backends': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
        },

        # задание 13.4 п.4
        'django.security': {
            'handlers': ['security_log'],
            'level': 'INFO',
        },
    },

}

# локализация
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]


MODELTRANSLATION_FALLBACK_LANGUAGES = ('en', 'ru')

