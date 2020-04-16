from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.news.parsers import avito

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')
celery_app.conf.update(flask_app.config)


@celery_app.task
def avito_snippets():
    print("Вход в habr_snippets()")
    with flask_app.app_context():
        avito.get_ads_snippets()


@celery_app.task
def habr_content():
    print("Вход в habr_content()")
    with flask_app.app_context():
        habr.get_news_content()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), avito_snippets.s())
    sender.add_periodic_task(crontab(minute='*/2'), habr_content.s())
