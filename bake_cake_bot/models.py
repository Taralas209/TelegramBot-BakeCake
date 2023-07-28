import uuid

from django.db import models
from django.utils import timezone


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Users(UUIDMixin, TimeStampedMixin):
    telegram_id = models.IntegerField(unique=True, default=False)
    username = models.CharField(
        max_length=64,
        null=True,
        verbose_name='User Name'
    )
    name = models.CharField(
        max_length=256,
        null=True,
        verbose_name='Name'
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        verbose_name='Phone Number'
    )
    is_admin = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name='Администратор'
    )
    registration = models.DateTimeField(default=timezone.now)


    def __str__(self):
        if self.username:
            return f'@{self.username}'
        else:
            return f'{self.telegram_id}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Order(models.Model):
    number = models.AutoField(
        verbose_name='Номер заказа',
        primary_key=True,
        unique=True
    )
    user = models.ForeignKey(
        Users, 
        on_delete=models.SET_NULL,
        null = True
    )
    price = models.FloatField(
        verbose_name='Цена',
        default=0.0
    )
    init_date = models.DateTimeField(
        verbose_name='Дата создания заказа',
        default=timezone.now()
    )
    delivery_date = models.DateTimeField(
        verbose_name='Дата и время доставки',
        default=None
    )
    address = models.TextField(
        verbose_name='Адрес доставки',
        max_length=500
    )
    promocode = models.CharField(
        verbose_name='Промокод',
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f'Заказ номер {self.number}'