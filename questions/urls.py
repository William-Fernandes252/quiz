from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path(
        "<int:question_id>",
        views.UserAnswerCreateForQuestionView.as_view(),
        name="useranswer-create-for-question",
    ),
    path("result", views.UserResultView.as_view(), name="user-result"),
    path("reset", views.ResetUserAnswersView.as_view(), name="user-reset-answers"),
]
