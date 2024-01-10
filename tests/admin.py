from django.contrib import admin

from .models import (
    Test,
    Question,
    Option,
    Answer,
    AnswerOption,
)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    pass
