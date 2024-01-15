from questions import forms, models


class TestUserAnswerForm:
    def test_it_sets_question_choices(self, question: models.Question):
        form = forms.UserAnswerForm(question=question)
        for answer in question.answers.all():
            assert answer in form.fields["answer"].queryset  # type: ignore
