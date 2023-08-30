from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


# Create your models here.
class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        p_rating = Post.objects.filter(author_id=self.pk).aggregate(sum_articles=Coalesce(Sum('article_rating') * 3, 0))['sum_articles']
        c_rating = Comment.objects.filter(id_user_id=self.name).aggregate(sum_article_rate=Coalesce(Sum('rating_comment'), 0))['sum_article_rate']
        post_cr = Comment.objects.filter(id_post__author__name=self.name).aggregate(sum_posts=Coalesce(Sum('rating_comment'), 0))['sum_posts']

        self.author_rating = p_rating + c_rating + post_cr
        self.save()

    def __str__(self):
        return f'{self.name.username}'


class Category(models.Model):
    subject = models.CharField(max_length=32, unique=True, verbose_name='Категория')

    def __str__(self):
        return f'{self.subject}'


class Post(models.Model):
    CAT_CHOICE = (('NW', 'Новость'), ('AR', 'Статья'))
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_type = models.CharField(max_length=2, choices=CAT_CHOICE, verbose_name='Категория')
    create_date = models.DateTimeField(auto_now_add=True)
    cat_subject = models.ManyToManyField(Category, through='PostCategory', verbose_name='Подкатегория')
    article_header = models.CharField(max_length=255, verbose_name='Заголовок')
    article_text = models.TextField(verbose_name='Текст статьи')
    article_rating = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def like(self):
        self.article_rating += 1
        self.save()

    def dislike(self):
        self.article_rating -= 1
        self.save()

    def preview(self):
        return f"{self.article_text[:250]} ..."

    def __str__(self):
        return f'{self.article_header}. Создана: {self.create_date}.   {self.article_text[:20]}'

    def get_absolute_url(self):
        return reverse('Post', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}  ---  {self.post}'


class Comment(models.Model):
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(verbose_name='Текст комментария')
    datatime_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.comment_text[:20]} - Создан: {self.datatime_comment}'

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()
