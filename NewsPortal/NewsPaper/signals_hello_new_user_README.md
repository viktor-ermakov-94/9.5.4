### Отправка письма после подтверждения электронной почты
#### в файле signals.py
    @receiver(email_confirmed)
    def user_signed_up(request, email_address, **kwargs):
        # отправляется письмо пользователю, чья почта была подтверждена
        send_mail(
            subject=f'Dear {email_address.user} Welcome to my News Portal!',
            message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
            from_email='FPW-13@yandex.ru',
            recipient_list=[email_address.user.email]
        )