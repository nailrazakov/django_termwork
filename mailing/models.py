from django.db import models
from django.utils import timezone
from users.models import User


class Client(models.Model):
    """Клиент сервиса"""
    email = models.EmailField(verbose_name='Почта', unique=True)
    fio = models.CharField(max_length=50, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий')
    phone = models.CharField(max_length=25, verbose_name='Телефон', blank=True, null=True)
    tg_nik = models.CharField(max_length=50, verbose_name='Телеграмм ник', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} - {self.fio}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """Сообщение для рассылки:"""
    #  Тема письма
    subject = models.CharField(max_length=150, verbose_name='Тема письма')
    #  Тело письма.
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Newsletter(models.Model):
    """Рассылка (настройки)"""

    STATUS = (
        ('created', 'создана'),
        ('launched', 'запущена'),
        ('completed', 'завершена'),
    )
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    PERIOD = (
        (DAILY, 'раз в день'),
        (WEEKLY, 'раз в неделю'),
        (MONTHLY, 'раз в месяц'),
    )
    #  Дата и время первой отправки рассылки;
    first = models.DateTimeField(auto_now_add=True, verbose_name='Первая рассылка')
    #  Дата и время последующих отправок рассылок
    follow_up = models.DateTimeField()
    #  Периодичность рассылки: раз в день, раз в неделю, раз в месяц;
    periodicity = models.CharField(max_length=15, choices=PERIOD, verbose_name='Периодичность рассылки')
    #  Статус рассылки (например, завершена, создана, запущена).
    status = models.CharField(max_length=15, choices=STATUS, default=STATUS[0][0], verbose_name='Статус рассылки')
    #  Рассылка внутри себя должна содержать ссылки на модели «Сообщения и «Клиенты сервиса».
    #  Сообщение у рассылки может быть только одно, а вот клиентов может быть много.
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', related_name='newsletters')
    owner = models.ForeignKey(User, verbose_name="Автор рассылки", help_text="Укажите автора рассылки", blank=True,
                              null=True, on_delete=models.CASCADE,)

    def __str__(self):
        return f"{self.periodicity} - {self.status}"

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Attempt(models.Model):
    """Модель 'Попытка рассылки'"""

    STATUS_OPTIONS = (
        ("successfully", "Успешно"),
        ("unsuccessfully", "Не успешно"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время попытки рассылки",
    )
    status = models.CharField(
        max_length=15, choices=STATUS_OPTIONS, default="successfully"
    )
    server_response = models.TextField(
        verbose_name="Ответ почтового сервера",
        blank=True,
        null=True,
    )
    mailing = models.ForeignKey(
        Newsletter,
        verbose_name="Рассылка",
        help_text="Укажите рассылку",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Автор рассылки",
        help_text="Укажите автора рассылки",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        ordering = ["created_at", "mailing", "status", "server_response"]
        permissions = [
            ("can_view_attempt_mailing", "Can view attempt mailing"),
        ]

    def __str__(self):
        return f"Рассылка запущена {self.created_at} автором - {self.owner}. Статус -  {self.status}."
