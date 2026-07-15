import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_post_created_notification(self, post_id: int, username: str):
    """
    Post yaratilganda background'da ishlaydigan task.
    Haqiqiy loyihada bu yerda email yuboriladi.
    """
    try:
        logger.info(
            f"[TASK] Yangi post yaratildi! "
            f"Post ID: {post_id} | Muallif: {username} | "
            f"Vaqt: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        # Haqiqiy loyihada:
        # send_mail(
        #     subject='Yangi post yaratildi',
        #     message=f'{username} yangi post yozdi. Post ID: {post_id}',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=['admin@example.com'],
        # )
        return {
            'status': 'success',
            'post_id': post_id,
            'author': username,
            'message': 'Bildirishnoma muvaffaqiyatli yuborildi.'
        }
    except Exception as exc:
        logger.error(f"[TASK ERROR] Post notification xatosi: {exc}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@shared_task
def check_old_posts():
    """
    Celery Beat tomonidan har 1 minutda ishlaydigan periodik task.
    30 kundan eski postlarni topadi va log yozadi.
    """
    from posting.models import Post

    threshold_date = timezone.now() - timezone.timedelta(days=30)
    old_posts = Post.objects.filter(created__lt=threshold_date).select_related('from_user')
    count = old_posts.count()

    logger.info(
        f"[BEAT TASK] Eski postlar tekshiruvi | "
        f"30+ kunlik postlar soni: {count} | "
        f"Tekshiruv vaqti: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return {
        'checked_at': timezone.now().isoformat(),
        'old_posts_count': count,
    }


@shared_task
def log_active_posts_count():
    """
    Har 5 minutda ishlaydigan task — bazadagi post sonini log qiladi.
    """
    from posting.models import Post

    total = Post.objects.count()
    logger.info(
        f"[BEAT TASK] Jami postlar soni: {total} | "
        f"Vaqt: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return {'total_posts': total}
