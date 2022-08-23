from django.db import models
from djchoices import ChoiceItem, DjangoChoices

from survey.models import Survey
from users.models import User


class OptionType(DjangoChoices):
    option1 = ChoiceItem('option1')
    option2 = ChoiceItem('option2')
    option3 = ChoiceItem('option3')
    option4 = ChoiceItem('option4')


class Question(models.Model):
    text = models.CharField('Question', max_length=1024)
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    correct_answer = models.CharField(
        max_length=128,
        choices=((name, name) for name, _ in OptionType.choices),
        verbose_name='correct answer',
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        verbose_name='survey',
        related_name='questions'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'questions'
        ordering = ['-creation_date']
