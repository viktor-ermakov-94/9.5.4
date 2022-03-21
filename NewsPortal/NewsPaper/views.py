from datetime import datetime, timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

# импортируем модель Post из models.py
from .models import Post, Category, PostCategory

# импортируем наш фильтр
from .search import PostFilter

# импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.core.paginator import Paginator

# импортируем созданную нами форму
from .forms import PostForm  # т.к. мы создали именно class PostForm(ModelForm)

# импортируем модель групп, redirect и декоратор проверки аутентификации.
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# для ограничения прав доступа импортируем соответствующий миксин
from django.contrib.auth.mixins import PermissionRequiredMixin

# для добавления новой статьи
from django.views.generic.edit import CreateView

# импортируем кэш
from django.core.cache import cache

# импортируем логгер
import logging

# импортируем функцию для локализации
from django.utils.translation import gettext as _

# импортируем "ленивый" геттекст с подсказкой
from django.utils.translation import pgettext_lazy

# импортируем часовые пояса
from django.utils import timezone
# импортируем стандартный модуль для работы с часовыми поясами
import pytz

logger = logging.getLogger(__name__)  # dundername берет название приложения, как имя логгера


def index(request):
    logger.info('INFO')


def debugger(request):
    logger.debug('DEBUG')


# создадим модель объектов, которые будем выводить
# Используется ListView - определяет список объектов, которые хотим отобразить.
# По умолчанию это просто даст нам все для модели, которую мы указали.
# Переопределив этот метод, мы можем расширить или полностью заменить эту логику.


class PostsList(ListView):
    # в данном случае рассматриваются все посты,
    # поэтому model = Post из файла models.py
    model = Post  # в нашем случае модель - Post (статья/новость)

    # зададим шаблон странички, в данном случае файл news.html
    # если не задать, то django автоматически выведет это имя из названия модели
    # и получится newspaper/post_list.html, которая всё-равно будет находится в папке templates
    template_name = 'newspaper/post_list.html'

    # также, можно указать название шаблона в поле context_object_name,
    # либо не указывать, тогда newspaper/post_list.html будет выбран по умолчанию, как шаблон
    context_object_name = 'post_list'

    # установим постраничный вывод на каждую новость через paginator
    paginate_by = 10

    # добавим ссылку на форму:
    form_class = PostForm



    # пишем модуль, который принимает на вход отфильтрованные объекты
    def get_context_data(self, **kwargs):
        # распаковываем self = Posts
        common_timezones = {
            'Europe/Paris': 'Paris',
            'Europe/Moscow': 'Moscow',
        }

        # context['categories'] = PostCategory.objects.all()

        return {
            **super().get_context_data(**kwargs),
            'current_time': timezone.localtime(timezone.now()),
            'timezones': common_timezones
        }

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


    # сортируем все объекты модели Post по параметру даты создания в обратном порядке:
    def get_queryset(self):
        qset = super().get_queryset()
        return qset.order_by('id', '-date_created')

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #
    #     return super().get(request, *args, **kwargs)

    # проверем, находится или нет пользователь в группе premium
    # делаем запрос на получение содержания (контекста)
    def get_context_data_2(self, **kwargs):
        # получаем весь контекст из класса родителя
        context = super().get_context_data_2(**kwargs)
        # добавляем новую переменную в Qset полученного контекста:
        # запрашиваем есть ли текущий пользователь в группе по фильтру author,
        # метод exists() вернет True, если группа premium находится в списке групп пользователя
        # not True даст False - а нам нужен True
        # если пользователь не находится в этой группе, то exist() вернет False. not False вернет True - то, что нужно
        context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        # context['is_not_premium'] = True

        # возвращаем контекст
        return context



class WeekList(ListView):
    model = Post
    template_name = 'newspaper/week_posts.html'
    context_object_name = 'week_posts'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        # получаем весь контекст из класса родителя
        context = super().get_context_data(**kwargs)
        return context


# пост детально
class PostDetailedView(DetailView):
    template_name = 'newspaper/post_details.html'
    queryset = Post.objects.all()

    # достаём объект из кэша
    def get_object(self, *args, **kwargs):
        # забираем значение из кэша по ключу, если ключа нет, то забираем None
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если в кэше нет объекта, то получаем его у класса родителя и записываем в кэш
        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


# создание поста
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'newspaper/post_create.html'
    form_class = PostForm
    permission_required = 'NewsPaper.add_post'
    # print(model.objects.all())


class PostSearch(ListView):
    model = Post  # в нашем случае модель - Post (статья/новость)
    template_name = 'newspaper/post_search.html'
    # context_object_name = 'post_search'
    paginate_by = 10
    form_class = PostForm

    # пишем модуль, который принимает на вход отфильтрованные объекты
    def get_context_data(self, **kwargs):
        # распаковываем self = Posts
        context = super().get_context_data(**kwargs)
        context['search'] = PostFilter(
            # в переменной request хранятся данные запроса
            self.request.GET,
            # Return the list of items for this view.
            queryset=self.get_queryset()
        )
        context['categories'] = PostCategory.objects.all()
        context['form'] = PostForm()
        return context


# напишем дженерик для редактирования новостей
class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'newspaper/post_create.html'
    form_class = PostForm
    permission_required = 'NewsPaper.change_post'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления новости
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'newspaper/post_delete.html'
    form_class = PostForm
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = 'NewsPaper.delete_post'


# функция добавляет пользователя в группу premium
@login_required  # upgrade_me = login_required(upgrade_me) декоратор проверяет if user is logged in
def upgrade_me(request):
    # запросим объект текущего пользователя пользователя из запроса
    user = request.user
    # получим группу 'author' из модели групп
    premium_group = Group.objects.get(name='author')
    # проверим, чтобы пользователь не состоят в группе 'author'
    if not request.user.groups.filter(name='author').exists():
        # раз пользователь в этой группе не состоит, добавим его туда
        premium_group.user_set.add(user)
    # при любом раскладе, перенаправляем пользователя на страницу со списком новостей, используя метод redirect
    return redirect('/news')


@login_required
def subscribe(request, **kwargs):  # request = <WSGIRequest: GET '/subscribe/'> - то есть к нам возвращается urls адрес,
    # который мы записали в html шаблоне кнопки
    pk = kwargs['pk']  # 0 то же самое можно записать, как: pk = kwargs.get('pk')

    my_post = Post.objects.get(id=pk).post_category.values()

    for i in my_post:
        # находим объекты категории, с которыми связан данный пост,
        # и добавляем текущего пользователя в поле subscribers моделей
        Category.objects.get(id=i['id']).subscribers.add(request.user)

    return redirect('/news')


class Index(View):
    def get(self, request):
        # Локализация времени
        current_time = timezone.now()

        # . Translators: This message appears on the home page only
        models = Category.objects.all()

        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'default.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')



