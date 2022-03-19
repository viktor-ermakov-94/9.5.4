from .models import Category, Post

# импортируем декоратор для перевода и класс настроек, от которого будем наследоваться
from modeltranslation.translator import register, TranslationOptions


# регистрируем наши модели для перевода
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    # указываем, какие именно поля надо переводить в виде кортежа
    fields = ('article_category',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title','content', )


