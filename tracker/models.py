from django.db import models
from .validators import (validate_summary_length, validate_no_test_word)
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True
    )

    name = models.CharField(max_length=255)

    description = models.TextField()

    users = models.ManyToManyField(
        User,
        related_name='projects',
        blank=True
    )


    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

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
    is_deleted = models.BooleanField(default=False)

    summary = models.CharField(
        max_length=255,
        validators=[
            validate_summary_length,
            validate_no_test_word
        ])

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

    types = models.ManyToManyField(
        Type, 
        verbose_name='Типы'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='issues'
    )

    def __str__(self):
        return self.summary