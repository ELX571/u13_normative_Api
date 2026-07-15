import os
from celery import Celery
from celery.schedules import crontab

# Django settings modulini belgilaymiz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('conf')

# Django settings'dan CELERY_ prefiksi bilan sozlamalarni olamiz
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha Django app'lardan task'larni avtomatik topamiz
app.autodiscover_tasks()

# ============================================================
# Celery Beat — Periodik tasklar jadvali
# ============================================================
app.conf.beat_schedule = {
    # Har 1 minutda eski postlarni tekshirish
    'check-old-posts-every-minute': {
        'task': 'posting.tasks.check_old_posts',
        'schedule': 60.0,  # 60 sekund = 1 minut
    },
    # Har 5 minutda jami post sonini log qilish
    'log-active-posts-every-5-minutes': {
        'task': 'posting.tasks.log_active_posts_count',
        'schedule': 300.0,  # 300 sekund = 5 minut
    },
    # Har kun tunda soat 00:00 da ishlaydigan task (crontab misoli)
    'daily-midnight-check': {
        'task': 'posting.tasks.check_old_posts',
        'schedule': crontab(hour=0, minute=0),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
