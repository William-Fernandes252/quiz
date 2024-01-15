from typing import Any

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView

from . import forms, models


class UserAnswerCreateForQuestionView(CreateView):
    model = models.UserAnswer
    form_class = forms.UserAnswerForm

    def get_initial(self) -> dict[str, Any]:
        question = get_object_or_404(models.Question, pk=self.kwargs["question_id"])
        return super().get_initial() | {
            "user": self.request.user,
            "question": question.statement,
        }

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs) | {
            "question_id": self.kwargs["question_id"]
        }

    def get_form(self, form_class=None) -> forms.UserAnswerForm:
        question = get_object_or_404(models.Question, pk=self.kwargs["question_id"])
        return self.form_class(question, **self.get_form_kwargs())

    def get_success_url(self) -> str:
        if not models.Question.objects.questions_not_answered_by_the_user(
            self.request.user
        ).exists():
            return reverse("questions:user-result")
        question_id = self.kwargs["question_id"]
        return reverse(
            "questions:useranswer-create-for-question",
            kwargs={"question_id": question_id + 1},
        )

    def get(self, request, *args, **kwargs):
        try:
            question = models.Question.objects.get(pk=self.kwargs["question_id"])
        except models.Question.DoesNotExist:
            if (
                models.Question.objects.questions_not_answered_by_the_user(
                    request.user
                ).count()
                > 0
            ):
                messages.error(request, "Questão não encontrada.")
            return redirect("questions:user-result")

        if models.UserAnswer.objects.filter(
            user=request.user, question=question
        ).exists():
            return redirect(
                reverse(
                    "questions:useranswer-create-for-question",
                    kwargs={"question_id": question.id + 1},
                ),
            )

        return super().get(request, *args, **kwargs)


class UserResultView(ListView):
    model = models.UserAnswer
    template_name = "questions/user_result.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["correct_answers"] = self.get_queryset().filter(is_correct=True).count()
        context["wrong_answers"] = self.get_queryset().filter(is_correct=False).count()
        return context

    def get(self, request, *args, **kwargs):
        if self.get_queryset().count() != models.Question.objects.count():
            return redirect("questions:useranswer-create-for-question", question_id=1)
        return super().get(request, *args, **kwargs)


class ResetUserAnswersView(View):
    def post(self, request, *args, **kwargs):
        models.UserAnswer.objects.filter(user=self.request.user).delete()
        return redirect("questions:useranswer-create-for-question", question_id=1)
