from django.db import models

from question.models import OptionType, Question
from survey.models import User


class Answer(models.Model):
    answer = models.CharField(
        max_length=128,
        choices=((name, name) for name, _ in OptionType.choices),
        verbose_name='correct answer',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='question',
        related_name='answer_question'
    )
    correct = models.BooleanField(null=True, blank=True)
    answered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Answered at'
    )
    respondent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    class Meta:
        verbose_name = 'answer'
        verbose_name_plural = 'answers'
        ordering = ['-answered_at']
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['respondent', 'question'],
        #         name='unique correspondent for question')
        # ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.question.correct_answer == self.answer:
            self.correct = True
        else:
            self.correct = False
        return super().save(force_insert, force_update, using, update_fields)
