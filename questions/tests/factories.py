from factory import Faker, SubFactory  # type: ignore
from factory.django import DjangoModelFactory  # type: ignore

from questions import models


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = models.Answer

    text = Faker("text")


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = models.Question

    statement = Faker("text")
    correct_answer = SubFactory(AnswerFactory)


class UserAnswerFactory(DjangoModelFactory):
    class Meta:
        model = models.UserAnswer

    user = SubFactory("users.tests.factories.UserFactory")
    answer = SubFactory(AnswerFactory)
    question = SubFactory(QuestionFactory)
