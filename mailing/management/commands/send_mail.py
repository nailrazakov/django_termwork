from smtplib import SMTPException

from django.utils import timezone
from django.core.mail import send_mail
from django.core.management import BaseCommand
from config import settings

from config.settings import EMAIL_HOST_USER
from mailing.models import Attempt, Newsletter


class Command(BaseCommand):
    """Отправка рассылки вручную через командную строку"""
    help = "Отправка почтовых уведомлений получателям"

    def handle(self, *args, **kwargs):
        newsletters = Newsletter.objects.all()
        for newsletter in newsletters:
            if newsletter and newsletter.status == 'created' or newsletter.status == 'launched':
                clients = newsletter.clients.all()
                for client in clients:
                    try:
                        send_mail(newsletter.message.subject, newsletter.message.body, EMAIL_HOST_USER, [client.email])
                        Attempt.objects.create(mailing=newsletter,
                                               status="successfully",
                                               server_response="Сообщение отправлено успешно",
                                               owner=settings.AUTH_USER_MODEL
                                               )
                    except SMTPException as e:
                        Attempt.objects.create(mailing=newsletter,
                                               status="unsuccessfully",
                                               server_response=str(e),
                                               owner=settings.AUTH_USER_MODEL)
            newsletter.status = "launched"
            newsletter.save()


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
                        status='successfully',
                        answer="Email отправлен",
                        owner=request.user
                    )
                    print(
                        f"Сообщение {mailing.message.subject} успешно отправлено на  {client.email}"
                    )
                except Exception as e:
                    Attempt.objects.create(
                        status='unsuccessfully',
                        answer=str(e),
                        owner=request.user
                    )
                    print(str(e))
            mailing.save()
