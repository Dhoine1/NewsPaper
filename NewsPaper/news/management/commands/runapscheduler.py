import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils.timezone import now
from news.models import Post, Category, Subscription
import datetime

logger = logging.getLogger(__name__)


def my_job():
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



# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")