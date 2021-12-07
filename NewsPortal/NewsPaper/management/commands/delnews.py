from django.core.management.base import BaseCommand, CommandError
from NewsPaper.models import Post


class Command(BaseCommand):
    help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    # missing_args_message = 'Недостаточно аргументов'
    # напоминать ли о миграциях
    requires_migrations_checks = True

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        self.stdout.readable()

        self.stdout.write(
            'Please choose post category')  # спрашиваем какую категорию почты удалить
        choise = input()  # считываем

        self.stdout.write(
            'Do you really want to delete all posts? yes/no')  # спрашиваем пользователя действительно ли он хочет
        # удалить все новости
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все посты указанной категории

            Post.objects.filter(post_category__article_category=choise).delete()

            self.stdout.write(self.style.SUCCESS('Posts are wiped!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим что в доступе отказано
