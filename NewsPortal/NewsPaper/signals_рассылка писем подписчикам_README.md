## D6.4 Subscribe
## Отправка писем при появлении новости соответствующей категории 

#### 1) я использовал шаблон post_details.html, куда добавил кнопку рядом с новостью ("Оформить подписку на подобные новости") 

    <td>
        <a class="nav-link" href="subscribe/">Оформить подписку на подобные новости </a>
    </td>

#### 2) после нажатия на эту кнопку, меня переносит по ссылке subscribe/
#### 3) далее срабатывает функция subscribe, которая прописана в urls/py

    ...
    path('<int:pk>/subscribe/', subscribe, name='subscription'),
    ...

#### 4) в файле NewsPaper\views.py добавляем функцию, которая запускается при нажатии на ссылку в шаблоне post_details.html
    
    # отправка писем для подписчиков по категориям
    @login_required
    def subscribe(request, **kwargs):  
        # request = <WSGIRequest: GET '/subscribe/'> - то есть к нам возвращается urls адрес,
        # который мы записали в html шаблоне кнопки

        pk = kwargs['pk']  # 0 то же самое можно записать, как: pk = kwargs.get('pk')
    
        my_post = Post.objects.get(id=pk).post_category.values()

        for i in my_post:
            post_cat_id = i['id']
 
        # находим объекты категории, с которыми связан данный пост,
        # и добавляем текущего пользователя в поле subscribers моделей
        Category.objects.get(id=post_cat_id).subscribers.add(request.user)
    
        subscribers = Category.objects.filter(subscribers=request.user)
        print(f"subscribed categories={subscribers}")
    
        for i in subscribers:
            print('Эта новость относится к категории:', i)
    
        print(my_post.filter(subscribers=request.user.id).exists())
    
        return redirect('/news')




#### 2. Создаем файл appointment\signals.py
в этом файле добавляем следующее:

#### 1) импортируем декоратор для получения сигналов
    from django.dispatch import receiver
#### 2) импортируем модуль для отправки писем менеджерам
    from django.core.mail import send_mail
#### 3) импортируем сигнал реагирующий на изменение поля ManyToMany в экземпляре модели
    from django.db.models.signals import m2m_changed
#### 4) импортируем модель Post, так как сигнал подключается к данной модели
    from .models import Post

#### 5) подключаемся к сигналу
    @receiver(m2m_changed, sender=Post.post_category.through)
    def new_post(sender, action, instance, **kwargs):
        # если проходит команда post_add, то есть добавляется новость,
        # то выполняются следующие действия:
        if action == 'post_add':
    
            # для каждого из экземпляров категорий созданной новости
            # (например,если у новости две категории, то для каждой из них)
            for each in instance.post_category.all():  # например в данном случае each -> sport, culture
                # потому что модель Category возвращает поле article_category, где как-раз хранятся значения sport и
                # culture instance - это экземпляр модели Category, и когда мы перебираем эти самые экземпляры,
                # то получаем доступ и к остальным полям. Поэтому в данном случае each представляет каждый
                # экземпляр instance
    
                # теперь мы снова перебираем поля экземпляра instance, который представлен переменной each
                # each.subscribers даёт нам доступ к полю subscribers, и следом вызывая cat.email, мы уже проваливаемся в
                # модель пользователя User к его родительскому классу, к полю email    
                for cat in each.subscribers.all():
                    # 1) cat = sport
                    # 2) cat = culture
    
                    send_mail(
                        subject=f'A new post named "{instance.title}" is created!',
                        message=f'{instance.date_created.strftime("%d %m %Y")} - {instance.content[:10]}',
                        from_email='FPW-13@yandex.ru',
                        recipient_list=[cat.email]
                    )
    
                    print(cat.email)


    <------------------------Примечания-------------------------->

    @receiver - это декоратор, который подключает приемник к сигналу.
    
    сигнал от создания -> post_save экземпляра Appointment
    
    класс Appointment является отправителем сигнала
    
    sender - модель, к которой подключен сигнал
    
    instance - экземпляр класса (модели) в базе данных (сущность)
    
    created - True, если модель была только что создана, False - если уже существует в базе данных
    
    **kwargs - сопутствующие словари, которые необходимо распаковать
    <------------------------Примечания-------------------------->

#### 6) в файл NewsPaper\apps.py добавляем функцию ready:

    def ready(self):
        import NewsPaper.signals