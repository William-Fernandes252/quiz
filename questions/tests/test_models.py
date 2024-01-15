from questions import models
from questions.tests import factories


class TestQuestion:
    def test_question_str(self, question: models.Question):
        assert question.__str__() == question.statement

    class TestSave:
        def test_it_sets_question_of_correct_answer(
            self, question: models.Question, db
        ):
            question.correct_answer = factories.AnswerFactory()
            question.save()
            assert question.correct_answer.question == question


class TestAnswer:
    def test_answer_str(self, answer: models.Answer):
        assert answer.__str__() == answer.text


class TestUserAnswer:
    class TestIsCorrect:
        def test_it_returns_true_if_answer_is_correct(
            self, user_answer: models.UserAnswer
        ):
            user_answer.answer = user_answer.question.correct_answer
            user_answer.save()
            assert user_answer.is_correct is True

        def test_it_returns_false_if_answer_is_not_correct(
            self, user_answer: models.UserAnswer
        ):
            user_answer.answer = factories.AnswerFactory()
            user_answer.save()
            assert user_answer.is_correct is False
