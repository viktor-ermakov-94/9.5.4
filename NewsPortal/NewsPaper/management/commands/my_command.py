from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Подсказка вашей команды'
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True

    # ввод в командной строке передается в этот метод и разбирается (парсится)
    # благодаря nargs="+" можно передать несколько аргументов подряд через пробел
    def add_arguments(self, parser):
        parser.add_argument('argument', nargs='+', type=str)

    # код, который выполняется при вызове команды
    def handle(self, *args, **options):
        self.stdout.write(str(options['argument']))