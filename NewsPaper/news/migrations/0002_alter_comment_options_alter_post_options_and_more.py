# Generated by Django 4.2.4 on 2023-08-22 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AlterField(
            model_name='category',
            name='subject',
            field=models.CharField(max_length=32, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.TextField(verbose_name='Текст комментария'),
        ),
        migrations.AlterField(
            model_name='post',
            name='article_header',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='post',
            name='article_text',
            field=models.TextField(verbose_name='Текст статьи'),
        ),
        migrations.AlterField(
            model_name='post',
            name='cat_subject',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category', verbose_name='Подкатегория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='news_type',
            field=models.CharField(choices=[('NW', 'Новость'), ('AR', 'Статья')], max_length=2, verbose_name='Категория'),
        ),
    ]
