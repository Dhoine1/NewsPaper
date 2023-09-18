from celery import shared_task
from django.core.mail import EmailMultiAlternatives
import datetime
from django.utils.timezone import now
from .models import Post, Subscription
from django.conf import settings


@shared_task
def send_notification(emails, subject, text_content, html_content):

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task()
def schedule_sending():
    week = now() - datetime.timedelta(days=7)
    posts = Post.objects.filter(create_date__gte=week)
    categories = set(posts.values_list('cat_subject__subject', flat=True))

    for cat in categories:
        subscribers = Subscription.objects.filter(category__subject=cat)
        emails = set([subs.user.email for subs in subscribers])
        list_to_send = ''
        list_to_send_text = ''

        cat_post_week = list(Post.objects.filter(cat_subject__subject__contains=cat, create_date__gte=week))
        for item_list in cat_post_week:
            list_to_send_text += f'-- {item_list.preview()} : Ссылка {settings.SITE_URL}/news/{item_list.pk} --'
            list_to_send += f'<a href={settings.SITE_URL}/news/{item_list.pk}> {item_list.preview()}</a><br><br>'

        for email in emails:
            title = f'Новости за неделю из категории: {cat}'
            msg = EmailMultiAlternatives(title, list_to_send_text, None, [email])
            msg.attach_alternative(list_to_send, "text/html")
            msg.send()
