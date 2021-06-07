from datetime import datetime, timezone

from django.shortcuts import render

# импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

# импортируем модель Post из models.py
from .models import Post, PostCategory

# импортируем наш фильтр
from .search import PostFilter

# импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.core.paginator import Paginator

# импортируем созданную нами форму
from .forms import PostForm  # т.к. мы создали именно class PostForm(ModelForm)


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
        context = super().get_context_data(**kwargs)
        context['categories'] = PostCategory.objects.all()
        return context

    # сортируем все объекты модели Post по параметру даты создания в обратном порядке:
    def get_queryset(self):
        qset = super().get_queryset()
        return qset.order_by('id', '-date_created')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


# пост детально
class PostDetailedView(DetailView):
    template_name = 'newspaper/post_details.html'
    queryset = Post.objects.all()


# создание поста
class PostCreateView(CreateView):
    template_name = 'newspaper/post_create.html'
    form_class = PostForm


class PostSearch(ListView):
    model = Post  # в нашем случае модель - Post (статья/новость)
    template_name = 'newspaper/post_search.html'
    #context_object_name = 'post_search'
    paginate_by = 10
    form_class = PostForm

    # пишем модуль, который принимает на вход отфильтрованные объекты
    def get_context_data(self, **kwargs):
        # распаковываем self = Posts
        context = super().get_context_data(**kwargs)
        context['search'] = PostFilter(
            self.request.GET,
            queryset=self.get_queryset()
        )
        context['categories'] = PostCategory.objects.all()
        context['form'] = PostForm()
        return context


# напишем дженерик для редактирования новостей
class PostUpdate(UpdateView):
    template_name = 'newspaper/post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления новости
class PostDelete(DeleteView):
    template_name = 'newspaper/post_delete.html'
    form_class = PostForm
    queryset = Post.objects.all()
    success_url = '/news/'

