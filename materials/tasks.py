import datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone


@shared_task
def send_course_update_email(email, course_id, course_title):
    send_mail(
        subject=f"Курс «{course_title}» обновлён",
        message=(f"Материалы курса «{course_title}» были обновлены. "
                 f"Посмотрите изменения в личном кабинете."),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """
    Проверяет пользователей по дате последнего входа и деактивирует неактивных.
    """
    # Определяем дату месяц назад от текущего момента с учетом timezone
    one_month_ago = timezone.now() - datetime.timedelta(days=30)

    # Получаем всех пользователей, чей last_login меньше, чем месяц назад
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)

    # Деактивируем найденных пользователей
    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"Пользователь {user.username} деактивирован из-за неактивности.")
