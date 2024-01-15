from computedfields.models import ComputedFieldsModel, computed  # type: ignore
from django.db import models


class QuestionManager(models.Manager):
    def not_answered_by_the_user(self, user):
        """Return questions not answered by the user."""
        return self.exclude(user_answers__user=user)


class Question(models.Model):  # type: ignore
    """Question for a quiz."""

    objects = QuestionManager()

    statement = models.TextField()
    correct_answer = models.OneToOneField(
        "Answer", on_delete=models.CASCADE, related_name="correct_answer_for"
    )

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if not self.correct_answer.question:
            self.correct_answer.question = self
            self.correct_answer.save()

    def __str__(self) -> str:
        """Return statement."""
        return self.statement


class Answer(models.Model):  # type: ignore
    """Answer for a quiz."""

    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="answers",
    )
    text = models.TextField()

    def __str__(self) -> str:
        """Return text."""
        return self.text


class UserAnswer(ComputedFieldsModel):
    """User answer for a quiz."""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE, related_name="users")
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="user_answers"
    )

    @computed(models.BooleanField(default=False))
    def is_correct(self):
        """Return True if user answer is correct."""
        return self.answer == self.question.correct_answer
