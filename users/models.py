from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email', help_text='Укажите ваш Email')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='avatar')
    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('can_view_users', 'Can view users'),
            ('can_users_is_active', 'Can users is active'),
        ]

    def __str__(self):
        return self.email
