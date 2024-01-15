import pytest
from django.test import RequestFactory
from pytest_mock import MockerFixture

from questions import models, views
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserAnswerCreateForQuestionView:
    class TestGetInitial:
        def test_it_returns_initial_data(
            self, question: models.Question, rf: RequestFactory
        ):
            request = rf.get("/")
            request.user = UserFactory()
            view = views.UserAnswerCreateForQuestionView(
                request=request, kwargs={"question_id": question.id}
            )
            assert view.get_initial() == {
                "question": str(question),
                "user": request.user,
            }

    class TestGetForm:
        def test_it_returns_form_with_question_as_arg(
            self, question: models.Question, rf: RequestFactory, mocker: MockerFixture
        ):
            request = rf.get("/")
            request.user = UserFactory()
            view = views.UserAnswerCreateForQuestionView(
                request=request, kwargs={"question_id": question.id}
            )
            form_mock = mocker.MagicMock()
            view.form_class = form_mock
            view.get_form()
            form_mock.assert_called_once_with(question, **view.get_form_kwargs())

    class TestGetSuccessUrl:
        def test_it_returns_user_result_url_if_no_questions_left(
            self, rf: RequestFactory
        ):
            request = rf.get("/")
            request.user = UserFactory()
            view = views.UserAnswerCreateForQuestionView(
                request=request, kwargs={"question_id": 1}
            )
            view.kwargs = {"question_id": 1}
            url = view.get_success_url()
            assert url == "/questions/result"

        def test_it_returns_next_question_url_if_questions_left(
            self, question: models.Question, rf: RequestFactory
        ):
            request = rf.get("/")
            request.user = UserFactory()
            view = views.UserAnswerCreateForQuestionView(
                request=request, kwargs={"question_id": 1}
            )
            view.kwargs = {"question_id": question.pk}
            url = view.get_success_url()
            assert url == f"/questions/{question.pk + 1}"
