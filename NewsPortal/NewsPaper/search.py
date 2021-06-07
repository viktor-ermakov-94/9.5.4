# импортируем filterset
from django_filters import FilterSet
# импортируем модель Post
from .models import Post


# создаём фильтр
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
