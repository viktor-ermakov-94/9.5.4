# импортируем декоратор для получения сигналов
from django.contrib.auth.models import User
from django.dispatch import receiver

# импортируем модуль для отправки писем
from django.core.mail import send_mail

# импортируем сигнал реагирующий на создание новой модели (в данном случае - новости)
from django.db.models.signals import post_save, m2m_changed

# импортируем модель Post, так как сигнал будет подключаться к ней
from . import views
from .models import Post#, Category, PostCategory


@receiver(m2m_changed, sender=Post.post_category.through)
def new_post(sender, action, instance, **kwargs):
    if action == 'post_add':
        print(instance.post_category.all())
        for i in instance.post_category.all():
            print(f'category.id {i.id}')
            print(f'category {i}')
            print(f'category.subscribers {i.subscribers.all()}')
        for j in i.subscribers.all():
            print(j.email)
            # send_mail(
            #             subject=f'A new post named "{instance.title}" is created!',
            #             message=f'{instance.date_created.strftime("%d %m %Y")} - {instance.content[:10]}',
            #             from_email='FPW-13@yandex.ru',
            #             recipient_list=[i.email ]
            #         )

    # # id = instance.pk
    # # print(id)
    # # if created:
    #     # for i in instance.post_category:
    #     #     print(i.subscribers)
    #     # for i in User.objects:
    #     #     if instance.post_category in instance.category:
    #         # send_mail(
    #         #     subject=f'A new post named "{instance.title}" is created!',
    #         #     message=f'{instance.date_created.strftime("%d %m %Y")} - {instance.content[:10]}',
    #         #     from_email='FPW-13@yandex.ru',
    #         #     recipient_list=['FPW-13@yandex.ru', ]
    #         # )
    #     all_posts = Post.objects.all()
    #
    #
    #     # print(f'all_posts: {all_posts}')
    #     # print(f'current post id: {instance.id}')
    #     # print(all_posts)
    #     # print(Post.objects.get(id=instance.id))
    #     # print(Post.objects.get(id=instance.id).post_category.values('article_category'))
    #     # for i in Post.objects.get(id=instance.id).post_category.values('article_category'):
    #     #     print(i)
    #     print(Post.objects.all())
    #     for i in Post.objects.all():
    #
    #         print(f'id:{i.id}, {i.post_category.values("article_category")}')
    #
    #     # print(Category.objects.values())
    #     # print(Category.objects.filter(article_category='sport'))
    #
    #     print(f'current news id is: {instance.id}')
    #
    #     p = Post.objects.filter(post_category__subscribers=170)
    #     print(p)
    #     # print(Post.objects.get(id=instance.id).post_category.values('subscribers'))
    #     # print(Category.objects.get(id=instance.id).values())


