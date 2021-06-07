# импортируем библиотеку для работы с путями urls
from django.urls import path
# импортируем наше представление
from .views import PostsList, PostDetailedView, PostCreateView, PostSearch, PostUpdate, PostDelete
from . import views

urlpatterns = [
    path('', PostsList.as_view()),

    # детали поста
    path('<int:pk>/', PostDetailedView.as_view(), name='post_details'),
    # создание поста
    path('create/', PostCreateView.as_view(), name='post_create'),

    path('search/', PostSearch.as_view(), name='post_search'),

    path('create/<int:pk>', PostUpdate.as_view(), name='post_update'),

    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
]

