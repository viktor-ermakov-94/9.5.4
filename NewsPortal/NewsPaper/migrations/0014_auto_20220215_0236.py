# Generated by Django 3.2.4 on 2022-02-14 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPaper', '0013_auto_20210806_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='article_category_en',
            field=models.CharField(help_text='category name', max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='article_category_ru',
            field=models.CharField(help_text='category name', max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='article_category',
            field=models.CharField(help_text='category name', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_category',
            field=models.ManyToManyField(related_name='post_category', to='NewsPaper.Category', verbose_name='category of the post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, verbose_name='title of the post'),
        ),
    ]
