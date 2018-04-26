from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contabilidad.contabilidad.settings')

app = Celery('contabilidad')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0, say_hello.s(), name='Say hello')


@app.task
def say_hello():
    pass
