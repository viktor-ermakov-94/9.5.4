# Пакет allauth для реализации регистрации через сторонние сайты
    pip install django-allauth

# settings.py
#### 1. Внесем изменения в файл настроек
Добавим в 'context_processors' строку, которая требуется для allauth:

    TEMPLATES = [
        {
            ....
            'OPTIONS': {
                'context_processors': [
                    ...
                    'django.template.context_processors.request',
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

    INSTALLED_APPS = [
        ...
        # для allauth добавляем следующие приложения
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        # добавляем провайдеров, которые необходимо подключить (например, Google):
        'allauth.socialaccount.providers.google',
    ]

Пропишем следующий путь:

    LOGIN_URL = '/accounts/login/'

SITE_ID используется в случае, если данный проект управляет несколькими сайтами, но для нас сейчас это не является принципиальным. Достаточно явно прописать значение 1 для этой переменной.

#### 2. Выполняем миграцию!

# Регистрация и вход по почте

## settings.py

#### 1. Добавим в настройки дополнительные параметры
    
# добавим настройки о том, что поле email является обязательным и уникальным
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_UNIQUE_EMAIL = True
    # поле username необязательно
    ACCOUNT_USERNAME_REQUIRED = False
    # укажем, что аутентификация будет происходить посредством электронной почты
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    # укажем, что верификация почты отсутствует (подтверждение аккаунта через письмо на почту)
    ACCOUNT_EMAIL_VERIFICATION = 'none'

# 2. В главный файл utls добавим путь к шаблону
    urlpatterns = [
        ...
        path('accounts/', include('allauth.urls')),    
        
    ]

# templates/base.html
#### Название файла должно быть именно таким!

    <!DOCTYPE html>
    <html>
        <head>
            <title>{% block head_title %}{% endblock head_title %}</title>
        </head>
        <body>
            {% block body %}
            {% block content %}
            {% endblock content %}
            {% endblock body %}
            {% block extra_body %}
            {% endblock extra_body %}
        </body>
    </html>