from django.db import models

class Status(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name


class Issue(models.Model):
    summary = models.CharField(
        max_length=255,
        verbose_name='Краткое описание'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Полное описание'
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='issues',
        verbose_name='Статус'
    )

    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        related_name='issues',
        verbose_name='Тип'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.summary