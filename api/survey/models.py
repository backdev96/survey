from django.db import models
from django.db.models.fields.related import ForeignKey
from users.models import User


class Survey(models.Model):
    author = ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    name = models.CharField('survey name', max_length=1024)
    description = models.CharField(
        'survey description',
        max_length=2048,
        blank=True,
        null=True
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )

    class Meta:
        verbose_name = 'survey'
        verbose_name_plural = 'surveys'
        ordering = ['-creation_date']

    def __str__(self):
        return f'{self.name}'
