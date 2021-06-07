from django.contrib import admin

# импортируем наши модели
from .models import Post
# и зарегистрируем их
admin.site.register(Post)

