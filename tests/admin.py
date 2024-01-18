from django.contrib import admin

from .models import (
    Test,
    Question,
    Option,
    Answer,
    Attempt,
)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "text", "right")
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    pass
