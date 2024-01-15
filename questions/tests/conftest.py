import pytest

from questions.tests import factories


@pytest.fixture
def question(db):
    """Returns question instance."""
    return factories.QuestionFactory()


@pytest.fixture
def answer(db):
    """Returns answer instance."""
    return factories.AnswerFactory()


@pytest.fixture
def user_answer(db):
    """Returns user answer instance."""
    return factories.UserAnswerFactory()
