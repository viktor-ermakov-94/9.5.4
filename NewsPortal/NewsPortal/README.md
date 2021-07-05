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
    
   
D5.5 Группы пользователей
Добавление в группы при регистрации
Сделаем так, чтобы пользователь при регистрации автоматически попадал в категорию basic:
# forms.py

# Добавление к группе (категории) пользователей сразу при регистрации
# Для этого:
#    Создадим модель BasicSignupForm, на основе модели из библиотеки allauth,
#    унаследовав модель SignupForm
class BasicSignupForm(SignupForm):

   # работаем с методом save()
   def save(self, request):
       # обходим через super() предков класса self -> BasicSignupForm
       # и user, который регистрируется в данный момент, сохраняется через вызов метода save() класса родителя
       # а в request содержится HTTP-запрос со страницы, которую пользователь заполняет в данный момент
       user = super().save(request)
       # запрашиваем объект с именем группы basic
       basic_group = Group.objects.get(name='basic')
       # и в этот объект с именем группы basic добавляем текущего user
       basic_group.user_set.add(user)
       # возвращаем пользователя
       return user


# settings.py
# чтобы allauth выполнил именно эту форму при регистрации пользователя, а не ту, что по умолчанию, напишем:
ACCOUNT_FORMS = {'signup': 'NewsPaper.forms.BasicSignupForm'}

Добавление в новые группы зарегистрированного пользователя
В модель вьюшки страницы, на которой нужно увидеть кнопку “Хочу в премиум”, нужно добавить функцию проверки находится ли пользователь в группе премиум или нет.
Я решил добавить кнопку на страницу списка новостей, поэтому добавил в модели этой вьюшки функцию:
# views.py
# проверем, находится или нет пользователь в группе premium
# делаем запрос на получение содержания (контекста)
def get_context_data(self, **kwargs):
   # получаем весь контекст из класса родителя
   context = super().get_context_data(**kwargs)
   # добавляем новую переменную в Qset полученного контекста:
   # запрашиваем есть ли текущий пользователь в группе по фильтру premium,
   # метод exists() вернет True, если группа premium находится в списке групп пользователя
   # not True даст False - а нам нужен True
   # если пользователь не находится в этой группе, то exist() вернет False. not False вернет True - то, что нужно
   context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
   # context['is_not_premium'] = True
   # возвращаем контекст
   return context
# default.py
в html-шаблон добавил кнопку, которая активна только если пользователь не состоит в группе премиум:
{% if is_not_premium %}
 <li class="nav-item">
   <button1> <a class="nav-link" href="sign/upgrade/">Хочу Premium!</a></button1>
 </li>
{% endif %}

# views.py
для того, чтобы физически добавить пользователя в группу premium, необходимо написать функцию:

# импортируем модель групп, redirect и декоратор проверки аутентификации.
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# функция добавляет пользователя в группу premium
@login_required # upgrade_me = login_required(upgrade_me) декоратор проверяет if user is logged in
def upgrade_me(request):
   # запросим объект текущего пользователя пользователя из запроса
   user = request.user
   # получим группу 'premium' из модели групп
   premium_group = Group.objects.get(name='premium')
   # проверим, чтобы пользователь не состоят в группе 'premium'
   if not request.user.groups.filter(name='premium').exists():
       # раз пользователь в этой группе не состоит, добавим его туда
       premium_group.user_set.add(user)
   # при любом раскладе, перенаправляем пользователя на страницу со списком новостей, используя метод redirect
   return redirect('/news')

# urls.py
# импортируем функцию, которую мы написали для добавления пользователя в группу premium
from .views import upgrade_me

# добавление пользователя в группу 'premium'
# получается, что срабатывает гиперссылка "sign/upgrade/", которую мы написали для кнопки "Хочу в Premium"
# в HTML-шаблоне default.html (<button1> <a class="nav-link" href="sign/upgrade/">Хочу Premium!</a></button1>)
# после того, как гиперссылка сработает, запускается функция upgrade_me
urlpatterns = [
...
path('sign/upgrade/', upgrade_me, name='upgrade'),
]


D5.6 Права доступа
view — просмотр объектов модели;
add — добавление объектов модели;
delete — удаление объектов модели;
change — изменить содержание объекта модели.
 
shop.view_product;
shop.add_product;
shop.delete_product;
shop.change_product.

<app>.<action>_<model>.
# view.py
# для ограничения прав доступа импортируем соответствующий миксин
from django.contrib.auth.mixins import PermissionRequiredMixin
Если хотим ограничить возможность добавления новостей, то добавляем в модель создания поста строку permission_required = 'NewsPaper.add_post.
Предварительно делаем настройки через админ-панель джанго, где выбираем возможности добавления постов для группы admin, и не выбираем такую возможность для группы common.
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
   model = Post
   template_name = 'newspaper/post_create.html'
   form_class = PostForm
   permission_required = 'NewsPaper.add_post'

Такую же проверку добавляем для возможности удаления поста:
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
   template_name = 'newspaper/post_delete.html'
   form_class = PostForm
   queryset = Post.objects.all()
   success_url = '/news/'
   permission_required = 'NewsPaper.delete_post'

Или для возможности редактирования поста:
class PostUpdate(PermissionRequiredMixin, UpdateView):
   template_name = 'newspaper/post_create.html'
   form_class = PostForm
   permission_required = 'NewsPaper.change_post'

   def get_object(self, **kwargs):
       id = self.kwargs.get('pk')
       return Post.objects.get(pk=id)
