from django.core.management.base import BaseCommand
from users.models import Payment
from materials.models import Course, Lesson
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Создание платежей"

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        Payment.objects.create(
            user=user, course=course, amount=1000.00, payment_method="cash"
        )
        Payment.objects.create(
            user=user, lesson=lesson, amount=500.00, payment_method="transfer"
        )
        self.stdout.write(self.style.SUCCESS("Платежи созданы"))
