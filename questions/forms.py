from crispy_forms.helper import FormHelper  # type: ignore
from crispy_forms.layout import HTML, Fieldset, Layout, Submit  # type: ignore
from django import forms

from . import models


class UserAnswerForm(forms.ModelForm):
    field_order = ["question", "answer"]
    label_suffix = ""
    helper = FormHelper()

    question: models.Question = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"disabled": True})
    )  # type: ignore

    class Meta:
        model = models.UserAnswer
        exclude = ["is_correct"]
        widgets = {
            "answer": forms.RadioSelect(),
            "user": forms.HiddenInput(),
        }

    def clean_question(self) -> models.Question:
        """Uses the question from the form to validate the answer."""
        return self.question

    def initialize_fields(
        self,
    ) -> None:
        """Initialize form with question and answers."""
        self.fields["question"].initial = self.question.statement
        self.fields["answer"].queryset = self.question.answers.all()  # type: ignore

    def __init__(self, question: models.Question, *args, **kwargs) -> None:
        """Initialize form with question and answers."""
        super().__init__(*args, **kwargs)
        self.question = question
        self.helper.form_id = "user-answer-form"
        self.helper.layout = Layout(
            Fieldset(
                HTML("<legend><h2>Questão {{ question_id }}</h3></legend>").html,
                "question",
                "answer",
            ),
            Submit("submit", "Enviar"),
        )
        self.helper.form_show_labels = False
        self.helper.render_hidden_fields = True
        self.initialize_fields()
