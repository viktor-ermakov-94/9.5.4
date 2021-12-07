

### Модуль D4.2.
GET-параметры в действии & django_filter & Paginator

Добавим страницу /news/search.
На ней должна быть реализована возможность пользователя искать новости по определённым критериям.
Критерии должны быть следующие:
позже какой-либо даты; 
по названию; 
по имени пользователя автора; 
всё вместе.
django_filter 
Действия: 
Установка пакета:
python -m pip install django-filter.
в файле settings.py, чтобы получить доступ к фильтрам в приложении добавляется в INSTALLED_APPS добавляем строку:
‘django_filters’
в папке, где находится models.py создется файл search.py;
в файле search.py пишем:
# импортируем filterset
from django_filters import FilterSet
# импортируем модель Post
from .models import Post
# создаём фильтр по указанным выше критериям
class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {
           # позже даты создания
           'date_created': ['gt'],

           # по названию
           'title': ['icontains'],

           # по автору
           'post_author': ['exact'],
           }
в файле views.py добавляем в модель PostLists:
# импортируем наш фильтр
from .search import PostFilter

# пишем модуль, который принимает на вход отфильтрованные объекты
def get_context_data(self, **kwargs):
   # распаковываем self = Posts
   context = super().get_context_data(**kwargs)
   context['search'] = PostFilter(
       self.request.GET,
       queryset=self.get_queryset()
   )
   return context


Добавьте постраничный вывод на основной странице новостей, чтобы на одной странице было не больше 10 новостей, и были видны номера лишь ближайших страниц, а также возможность перехода к первой или последней странице.
в html=шаблоне основной страниц добавим:
<!-- Перед таблицей добавим форму для поиска -->
<form method="GET">
   {{ search.form }} <!-- Форму от фильтров за нас сделает django.
   А вот кнопку, увы придётся делать самому -->
   <input type="submit" value="Найти">
</form>

для того, чтобы фильтр работал, перед выводом атрибутов модели post
добавляем строку:
{% for post in search.qs %} <!-- итерация фильтра -> search.qs передает отфильтрованные post-ы -->
чтобы были видны номера ближайших страниц, в конце шаблона добавляем:
<div class="pagination">
   <span class="step-links">
       {% if page_obj.has_previous %}
           <a href="?page=1">&laquo; Начало </a>
           <a href="?page={{ page_obj.previous_page_number }}"> <<< </a>
       {% endif %}

       <span class="current">
           Стр {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}.
       </span>

       {% if page_obj.has_next %}
           <a href="?page={{ page_obj.next_page_number }}"> >>> </a>
           <a href="?page={{ page_obj.paginator.num_pages }}"> Конец &raquo;</a>
       {% endif %}
   </span>
</div>

Paginator
Действия:
в модель, которая сделана на основе дженерика ListView, добавляем строку:
# установим постраничный вывод на каждую новость
paginate_by = 10

##Создание форм на основе ModelForms

####Создадим форму создания модели
1. В папку с приложением добавим файл <b> forms.py </b>.
В нём напишем следующее:
    
    
    from django.forms import ModelForm
    from .models import Post
        
    class PostForm(ModelForm):
        class Meta:
            model = Post
            fields = ['title', 'post_author', 'post_category']

2. Теперь эту модель PostForm нужно загрузить во вьюшку.
В файл <b> views.py </b> добавим:
    
* импортируем созданную нами форму
    
        
    from .forms import PostForm  # т.к. мы создали именно class PostForm(ModelForm)  

    
* в модель <b> class PostsList(ListView) </b> добавляем форм класс, 
чтобы получать доступ к форме через метод POST

    
    form_class = PostForm

 

* в ту же модель <b> class PostsList(ListView) </b> добавим модуль post


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  
         if form.is_valid():
            form.save()
         return super().get(request, *args, **kwargs)

3. В файл post_list.html добавим конструкцию POST


    <form method="POST">
        {% csrf_token %}
        {{ form }} <!-- Теперь нам нужна только готовая форма и кнопка -->
        <input type="submit" value="Добавить пост">
    </form>



##Создадим форму детального просмотра модели
####HTML
####post_details.html
В корневой директории проекта в папке создадим файл:
<b>templates/(название приложения)/post_details.html</b>
    
    <! -- наследование шаблона default -->
    {% extends 'flatpages/default.html' %}
     
    {% block title %} Post details {% endblock title %}
     
    {% block content %}
    {% if object_list %}
        <table>
            <tr>
                <td>
                    <b>
                        № поста
                    </b>
                </td>
                <td>
                    <b>
                        Заголовок
                    </b>
                </td>
    
                <td>
                    <b>
                        Дата публикации в формате (день.месяц.год)
                    </b>
                </td>
                <td>
                    <b>
                        Первые 20 слов текста статьи
                    </b>
                </td>
            </tr>
            {% for post in search.qs %} <!-- итерация фильтра -> search.qs передает отфильтрованные post-ы -->
            <tr>
                <td>
                    {{ post.id }}
                </td>
    
                <td>
                    {{ post.title|default:"Без заголовка"|truncatewords:4|censor:'***' }}
                </td>
                <td>
                    {{ post.date_created|default:"Без даты" }}
                </td>
                <td>
                    {{ post.content|truncatechars:20|censor:'***' }}
                </td>
            {% endfor %}
            </tr>
        </table>
    {% else %}
    <h2>
        Новостей нет!
    </h2>
    {% endif %}
    {% endblock content %}

####Django
в файле view.py добавим новый класс дженерик для <b>получения развернутой статьи</b>
1) Дженерик, создающий представление (View) просмотра новости/продукта
или чего-то ещё детально/подробно


    class PostDetailedView(DetailView):
        template_name = 'NewsPaper/post_detail.html'
        queryset = Post.objects.all()


2) Дженерик для создания поста:
   

    # создание поста
    class PostCreateView(CreateView):
        template_name = 'newspaper/post_create.html'
        form_class = PostForm

3) Дженерик для поиска поста:


    class PostSearch(ListView):
        model = Post  # в нашем случае модель - Post (статья/новость)
        template_name = 'newspaper/post_search.html'
        context_object_name = 'post_search'
        paginate_by = 10
        form_class = PostForm

        # пишем модуль, который принимает на вход отфильтрованные объекты
        def get_context_data(self, **kwargs):
            # распаковываем self = Posts, представляющий из себя QuerySet
            context = super().get_context_data(**kwargs)
            
            context['search'] = PostFilter(
                self.request.GET,
                queryset=self.get_queryset()
            )
            context['categories'] = PostCategory.objects.all()
            context['form'] = PostForm()
            return context






#### urls.py

В файле urls.py добавим путь к страничке, которые будут генерироваться следуя шаблонам

    path('<int:pk>/', PostDetailedView.as_view(), name='post_details'),

<br>
<br>
<br>
<br>

### <b>Cоздание поста</b>

####HTML
#### product_create.html
Создать файл в директории
<b>templates/(название приложения)/product_create.html</b>

    <! -- наследование шаблона default -->
    {% extends 'flatpages/default.html' %}
     
    {% block title %} Post List {% endblock title %}
     
    {% block content %}
    <h3>Информация о статье</h3>
    <form method="POST">
        {% csrf_token %} 
        {{ form }} <!-- Теперь нам нужна только готовая форма и кнопка -->
        <input type="submit" value="Запостить!">
    </form>
    {% endblock content %}

#### views.py

    class PostCreateView(CreateView):
        template_name = 'NewsPaper/post_create.html'
        form_class = PostForm

#### urls.py
Есть два файла urls.py:
1) находится в папке всего проекта (NewsPortal) 
   и является входным окном в приложение - <b>urls.py</b> 
2) находится в папке самого приложениея (NewsPaper) 
   и является продолжением входного окна, 
   приводящим к конечной странице - <b>app/urls.py</b> 
   
<b>urls.py</b>

    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
    
        # чтобы адреса в будущем написанных нами страничек были доступны
        # нам для перехода по ним, добавим путь:
        path('pages/', include('django.contrib.flatpages.urls')),
    
        # чтобы все адреса из файла urls.py самого приложения
        # автоматически подключались, добавим:
        path('news/', include('NewsPaper.urls')),
        # таким образом, будет получен доступ к путям из файла app/urls.py
    ]
  


<br>
<b>app/urls.py</b>

В файле urls.py добавим путь к страничке, которые будут генерироваться следуя шаблонам

    # импортируем библиотеку для работы с путями urls
    from django.urls import path
    
    # импортируем наше представление
    from .views import PostsList, PostDetailedView, PostCreateView, PostSearch, PostUpdate, PostDelete
    from . import views
    
    # пропишем пути к страничкам
    urlpatterns = [
        
        # главная страница (post_details.html)
        path('', PostsList.as_view()),
    
        # это страничка самого поста, если в него провалиться
        path('<int:pk>/', PostDetailedView.as_view(), name='post_details'),
        
        # создание поста
        path('create/', PostCreateView.as_view(), name='post_create'),
        
        # поиск поста
        path('search/', PostSearch.as_view(), name='post_search'),
        
        # редактирование поста (используется тот же шаблон, что и для создания, 
        # но другое представление
        path('create/<int:pk>', PostUpdate.as_view(), name='post_update'),
        
        # удаление поста
        path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    
    ]

####models.py
в модель Post добавим абсолютный путь, чтобы после создания нас перебрасывало на главную страницу с новостями

    def get_absolute_url(self):  
        return f'/news/{self.id}'
<br>
<br>
<br>
<br>

### Добавление гиперссылки
####в файле post_list.html внесём изменения:

добавим строчку: <b>a href="{% url 'post_details' post.id %}"</b>, чтобы сделать из неё гиперссылку

    <td>
        <a href="{% url 'post_details' post.id %}"> {{ post.title|default:"Без заголовка"|truncatewords:4|censor:'***' }}
    </td>


<br>
<br>
<br>
<br>





### Рабочий paginator из интернета
цикл должен пробегаться не по отфильтрованным search.qs, 
а по object_list:<b>
{% for post in object_list %}
</b>
1. Создать файл: <b>(app)/templatetags/my_tags.py</b>



    from django import template
    register = template.Library()

    @register.simple_tag(takes_context=True)
    def param_replace(context, **kwargs):
        d = context['request'].GET.copy()
        for k, v in kwargs.items():
            d[k] = v
        for k in [k for k, v in d.items() if not v]:
            del d[k]
        return d.urlencode()

2. 

    
    {% load my_tags %}
    {% if is_paginated %}
      {% if page_obj.has_previous %}
        <a href="?{% param_replace page=1 %}">First</a>
        {% if page_obj.previous_page_number != 1 %}
          <a href="?{% param_replace page=page_obj.previous_page_number %}">Previous</a>
        {% endif %}
      {% endif %}
      Page {{ page_obj.number }} of {{ paginator.num_pages }}
      {% if page_obj.has_next %}
        {% if page_obj.next_page_number != paginator.num_pages %}
          <a href="?{% param_replace page=page_obj.next_page_number %}">Next</a>
        {% endif %}
        <a href="?{% param_replace page=paginator.num_pages %}">Last</a>
      {% endif %}
      <p>Objects {{ page_obj.start_index }}—{{ page_obj.end_index }}</p>
    {% endif %}



### D7.5. Создание задач по расписанию
#### Библиотека Celery
1. Войти в виртуальное окружение:


    $ source virtualenv/bin/activate

2. Установить _Celery_:


    (virtualenv) $ pip3 install celery

3. В директории проекта добавить файл _celery.py_ рядом с _settings.py_.
   
4. В _celery.py_ добавить следующее:
   
    
    import os
    from celery import Celery
     
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
     
    app = Celery('project_name')
    app.config_from_object('django.conf:settings', namespace = 'CELERY')
    
    app.autodiscover_tasks()

    app.conf.beat_schedule = {
    
        'action_every_monday_8am': {
            'task': 'NewsPaper.newsletter.tasks.week_post',
            'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    
        },
    }

<i> В первую очередь мы импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery.

Второй строчкой мы связываем настройки Django с настройками Celery через переменную окружения.

Далее мы создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации. 

Мы также указываем пространство имен, чтобы Celery сам находил все необходимые настройки в общем конфигурационном файле settings.py. Он их будет искать по шаблону «CELERY_***».

Последней строчкой мы указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта.
</i>

5. Добавить следующие строки в файл `__init__.py` (рядом с _settings.py_):


    from .celery import app as celery_app
    
    __all__ = ('celery_app',)

6. Настроить _Celery_ по инструкции “First Steps With Django”:
В файле _settings.py_ добавить:


    CELERY_TIMEZONE = "Europe/Moscow"
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60

7. Далее нам нужно настроить поддержку _Redis_ в _Python_ и _Celery_. Вновь зайдите в виртуальное окружение и установите следующие пакеты:


    (virtualenv) $ pip3 install redis
    (virtualenv) $ pip3 install -U "celery[redis]"
 
8. Далее мы должны добавить некоторые настройки в конфигурацию проекта (_settings.py_), дописав следующие строки:


    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

9. Подключить tasks, чтоб <i>Celery</i> их нашёл (опционально):


    CELERY_IMPORTS = (
         'NewsPaper.newsletter.tasks',
    )

10. В папке проекта создать файл <i>docker-compose.yml</i> и добавим туда следующие строки:
    

    version: "3"
    
    
    services:
     redis:
       image: redis
       ports:
         - "6379:6379"
    
11. Установить _django-celery-beat_, _django-celery-results_

12. Добавить в _settings.py_
    

    INSTALLED_APPS = [
       ...
    
    'django_celery_beat',
    'django_celery_results',
    
    
    ]

		
### Для запуска задач по расписанию необходимо сделать следующее:

**Терминал 1: $ python manage.py runserver**

**Терминал 2: $ docker-compose up**

**Терминал 3: $ celery -A NewsPortal beat**

**Терминал 4: $ celery -A NewsPortal worker -l INFO --pool=solo**

##Дополнительные материалы:
Периодические задачи: [https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)

First Steps With Django: [https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html?highlight=Django](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html?highlight=Django)

Настройка Docker, Celery для очереди задач: [https://www.youtube.com/watch?v=hQEHONHcF2c&list=LL&index=2](https://www.youtube.com/watch?v=hQEHONHcF2c&list=LL&index=2)

Команды для запуска Celery: [https://medium.com/analytics-vidhya/python-celery-explained-for-beginners-to-professionals-part-3-workers-pool-and-concurrency-ef0522e89ac5](https://medium.com/analytics-vidhya/python-celery-explained-for-beginners-to-professionals-part-3-workers-pool-and-concurrency-ef0522e89ac5)