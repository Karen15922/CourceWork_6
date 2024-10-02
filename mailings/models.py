from users.models import User
from django.db import models
from django.utils import timezone

# константа для полей с возможно нулевыми значениями
NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель клиента рассылки
    """
    first_name = models.CharField(
        max_length=150, verbose_name="имя", default=None)
    last_name = models.CharField(
        max_length=150, verbose_name="фамилия", default=None)
    pantronymic = models.CharField(
        max_length=150, verbose_name="отчество", **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта', default=None)
    comment = models.TextField(
        max_length=100, verbose_name="Комментарий", **NULLABLE)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создатель клиента',
        **NULLABLE,
    )

    def __str__(self):
        return f'{self.email}'


class Message(models.Model):
    """
    Модель сообщения для рассылки
    """

    title = models.CharField(
        max_length=100,
        verbose_name="Тема сообщения",
    )
    content = models.TextField(verbose_name="Сообщение", **NULLABLE)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель сообщения",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("id",)

    def __str__(self):
        return self.title


class Mailing(models.Model):
    '''
    модель рассылки
    '''
    periodicity_list = [
        ("однократно", "однократно"),
        ("ежедневно", "ежедневно"),
        ("еженедельно", "еженедельно"),
        ("ежемесячно", "ежемесячно"),
    ]

    status_list = [
        ("complited", "complited"),
        ("created", "created"),
        ("active", "active"),
    ]

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='дата создания рассылки',
        **NULLABLE)

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name='сообщения',
        related_name='message',
        **NULLABLE
    )

    clients = models.ManyToManyField(
        Client,
        verbose_name="клиенты",
        related_name='clients'
    )

    periodicity = models.CharField(
        max_length=30,
        choices=periodicity_list,
        verbose_name="периодичность рассылки",
        default="однократно",
    )

    status = models.CharField(
        verbose_name="статус",
        max_length=30,
        choices=status_list,
        default="created",
    )
    next_date = models.DateTimeField(
        verbose_name="дата и время следующей отправки отправки",
        auto_now_add=True
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель рассылки",
        related_name='mailing_creator',
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_edit_status", "can_edit_status"),
        ]
        ordering = ("id",)

    def __str__(self):
        return f'Рассылка "{self.pk}"'


class Mailing_attempt(models.Model):
    """
    Модель попытки отправки рассылки
    """

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="рассылка",
        related_name="mailing",
    )

    last_attempt = models.DateTimeField(
        verbose_name="дата и время последней попытки",
        auto_now_add=True,
    )

    status = models.CharField(
        max_length=30,
        verbose_name="статус попытки",
        default="fail",
    )

    smtp_service_report = models.TextField(
        verbose_name="ответ почтового сервиса",
        **NULLABLE
    )

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "попытки"

    def __str__(self):
        return f'mailing attempt pk:{self.pk}'
