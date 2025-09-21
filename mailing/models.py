from django.db import models
from django.utils import timezone


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
    CREATED = 'created'
    LAUNCHED = 'launched'
    COMPLETED = 'completed'
    STATUS = (
        (CREATED, 'создана'),
        (LAUNCHED, 'запущена'),
        (COMPLETED, 'завершена'),
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
    status = models.CharField(max_length=15, choices=STATUS, default=CREATED, verbose_name='Статус рассылки')
    #  Рассылка внутри себя должна содержать ссылки на модели «Сообщения и «Клиенты сервиса».
    #  Сообщение у рассылки может быть только одно, а вот клиентов может быть много.
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', related_name='newsletters')

    def __str__(self):
        return f"{self.periodicity} - {self.status}"

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Attempt(models.Model):
    """Попытка рассылки:"""
    SUCCESSFULLY = 'success'
    FAILED = 'failed'
    STATUS = (
        (SUCCESSFULLY, 'успешно'),
        (FAILED, 'не успешно'),
    )
    #  дата и время последней попытки;
    last = models.DateTimeField(default=timezone.now, verbose_name="Последняя попытка")
    #  статус попытки (успешно / не успешно);
    status = models.CharField(choices=STATUS, default=FAILED, verbose_name='Статус попытки')
    #  ответ почтового сервера, если он был.
    answer = models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервиса')
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f"{self.last} - {self.status}"

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
