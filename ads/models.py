from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ad(models.Model):

    CONDITION_CHOICES = [
        ('new', 'Новая'),
        ('like_new', 'Почти как новая'),
        ('used', 'Б/у'),
        ('poor', 'Сильно поношенная'),
        ('broken', 'Сломанная (на запчасти)'),
    ]

    user = models.ForeignKey(
        User, models.CASCADE, "ads", verbose_name='Владелец',
    )
    title = models.CharField("Заголовок", max_length=500)
    description = models.TextField("Описание")
    image_url = models.ImageField(
        "Фото", upload_to="ads/%Y/%m/%d", blank=True, null=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True, related_name='ads')
    condition = models.CharField(
        "Состояние", max_length=15, choices=CONDITION_CHOICES)
    created_at = models.DateField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return f"{self.title}({self.id})"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принята"),
        ("rejected", "Отклонена"),
    ]

    ad_sender = models.ForeignKey(
        "ads.Ad",
        on_delete=models.CASCADE,
        related_name="proposals_sent"
    )
    ad_receiver = models.ForeignKey(
        "ads.Ad",
        on_delete=models.CASCADE,
        related_name="proposals_received"
    )
    comment = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Комментарий"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
        ordering = ["-created_at"]
        unique_together = ["ad_sender", "ad_receiver", "status"]

    def __str__(self):
        return f"Обмен {self.ad_sender} на {self.ad_receiver} ({self.status})"
