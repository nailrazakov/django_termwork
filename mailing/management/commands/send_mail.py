from django.utils import timezone
from django.core.mail import send_mail
from django.core.management import BaseCommand

from config.settings import EMAIL_HOST_USER
from mailing.models import Attempt, Newsletter


class Command(BaseCommand):
    """Отправка рассылки вручную через командную строку"""
    help = "Отправка почтовых уведомлений получателям"

    def handle(self, *args, **kwargs):
        mailings = Newsletter.objects.filter(
            status__in=[Newsletter.created, Newsletter.launched]
        )
        for mailing in mailings:
            for client in mailing.clients.all():
                try:
                    send_mail(
                        mailing.message.subject,
                        mailing.message.body,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )
                    Attempt.objects.create(
                        data=timezone.now(),
                        sending_status=Attempt.successfully,
                        answer="Email отправлен",
                        status=mailing,
                    )
                    print(
                        f"Сообщение {mailing.message.subject} успешно отправлено на  {client.email}"
                    )
                except Exception as e:
                    Attempt.objects.create(
                        sending_status=Attempt.unsuccessfully,
                        answer=str(e),
                        status=mailing,
                    )
                    print(str(e))
            mailing.save()
