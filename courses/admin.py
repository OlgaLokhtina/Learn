from django.contrib import admin
from .models import (
    Course,
    TypeBlock,
    Block,
    CourseView,
    Test,
    Question,
    Option,
    Answer,
    AnswerOption,
)


@admin.register(TypeBlock)
class TypeBlockAdmin(admin.ModelAdmin):
    list_display = ["name"]


class BlockInline(admin.StackedInline):
    model = Block
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "id"]
    fields = ["title", "description", "preview", ("order", "created")]
    search_fields = ["title"]
    inlines = [BlockInline]
    readonly_fields = ["created"]


@admin.register(CourseView)
class CourseViewAdmin(admin.ModelAdmin):
    list_display = ["user", "course", "date"]
    list_filter = ["user", "course"]
    readonly_fields = ["user", "course", "date"]


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
