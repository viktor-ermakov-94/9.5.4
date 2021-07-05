from django.forms import ModelForm, BooleanField
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Галочка')  # добавляем галочку, или же true-false поле

    class Meta:
        model = Post  # это модель, по которой будет строиться форма

        # поля, которые будут выводиться на страничке
        fields = ['title', 'post_author', 'post_category', 'check_box']


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
        basic_group = Group.objects.get(name='common')
        # и в этот объект с именем группы basic добавляем текущего user
        basic_group.user_set.add(user)
        # возвращаем пользователя
        return user