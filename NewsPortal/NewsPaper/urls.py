# импортируем библиотеку для работы с путями urls
from django.urls import path
# импортируем наше представление
from .views import PostsList, PostDetailedView, PostCreateView, PostSearch, PostUpdate, PostDelete
from . import views
# импортируем функцию, которую мы написали для добавления пользователя в группу premium
from .views import upgrade_me, subscribe


urlpatterns = [
    path('', PostsList.as_view(), name='home'),

    # детали поста
    path('<int:pk>/', PostDetailedView.as_view(), name='post_details'),
    # создание поста
    path('create/', PostCreateView.as_view(), name='post_create'),

    path('search/', PostSearch.as_view(), name='post_search'),

    path('create/<int:pk>', PostUpdate.as_view(), name='post_update'),

    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    # добавление пользователя в группу 'premium'
    # получается, что срабатывает гиперссылка "sign/upgrade/", которую мы написали для кнопки "Хочу в Premium"
    # в HTML-шаблоне default.html (<button1> <a class="nav-link" href="sign/upgrade/">Хочу Premium!</a></button1>)
    # после того, как гиперссылка сработает, запускается функция upgrade_me
    path('sign/upgrade/', upgrade_me, name='upgrade'),

    path('<int:pk>/subscribe/', subscribe, name='subscription'),
    #path('subscribe/', subscribe, name='subscription'),



]

