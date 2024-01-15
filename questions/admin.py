from computedfields.admin import ComputedModelsAdmin  # type: ignore
from django.contrib import admin

from .models import Answer, Question, UserAnswer


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ("id", "statement", "correct_answer")


class UserAnswerAdmin(ComputedModelsAdmin):
    list_display = ("user", "answer", "question", "is_correct")
    list_filter = ("user", "question", "answer")
    search_fields = ("user__username", "question__statement", "answer__text")
    readonly_fields = ("is_correct",)

    def has_add_permission(self, request):
        return False  # Disable adding UserAnswer instances through the admin interface


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(UserAnswer, UserAnswerAdmin)
