from django.contrib import admin

# импортируем наши модели
from .models import Post, Category, Author

# импортируем модель амдинки
from modeltranslation.admin import TranslationAdmin


def delete_posts(self, request, queryset):
    Post.objects.all().delete()


# создадим новый класс для представления постов в админ панели
# class PostsAdmin(admin.ModelAdmin):
#     # выводим параметр list_display из ModelAdmin, который отображает все поля модели
#     # почему-то list_display не принимает ManyToMany Field, а list_filter принимает. В связи с чем, чтобы вывести article_category нужно зайти через Post.post_category
#     list_display = ('pk', 'date_created', 'title', 'category', 'zero_rated', 'article_category',)
#
#     # фильтр справа
#     list_filter = ('category', 'post_category',)
#
#     # поисковый фильтр
#     search_fields = ('title',)
#
#     # создание нестандартных команд
#     actions = [delete_posts]
#
#     def article_category(self, Post):
#         return [i for i in Post.post_category.all()]


# локализация
class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

# и зарегистрируем их
# admin.site.register(PostsAdmin)
# admin.site.register(Category)
admin.site.register(Author)
# admin.site.register(Post)