from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory, Subscription
from django.conf import settings
from .tasks import send_notification


@receiver(m2m_changed, sender=PostCategory)
def product_created(instance, action, **kwargs):
    if action == 'post_add':

        categories = instance.cat_subject.all()
        emails = []

        for cat in categories:
            subscribers = Subscription.objects.filter(category=cat)
            emails += [subs.user.email for subs in subscribers]

        subject = f'Новая публикация в разделе, на который вы подписаны.'

        text_content = (
            f'Название: {instance.article_header}\n'
            f'Preview: {instance.preview()}\n\n'
            f'Ссылка на публикацию: {settings.SITE_URL}/news/{instance.pk}'
        )
        html_content = (
            f'Название: {instance.article_header}<br>'
            f'Preview: {instance.preview()} <br><br>'
            f'<a href="{settings.SITE_URL}/news/{instance.pk}">'
            f'Ссылка на публикацию</a>'
        )
        send_notification(emails, subject, text_content, html_content)

        #
        # for email in emails:
        #     msg = EmailMultiAlternatives(subject, text_content, None, [email])
        #     msg.attach_alternative(html_content, "text/html")
        #     msg.send()
