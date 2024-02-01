from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

from .forms import QuestionForm

from django.views.generic import ListView

from tests.models import (
    Test,
    Question,
    Option,
    Answer,
    Attempt,
)
from users.models import User

# Create your views here.
class TestView(ListView):
    model = Test
    context_object_name = "tests"
    template_name = "test.html"


def test(request, pk):
    test = Test.objects.get(id=pk)
    return render(request, "test_pass.html", {"test": test})


def test_attempt(request, pk):
    test = Test.objects.get(id=pk)
    if request.method == "GET":
        at = Attempt.objects.create(user=request.user, test=test)
        request.session["it"] = str(at.id)
        page_number = 1
    else:
        at = Attempt.objects.get(id=int(request.session.get("it")))
        page_number = request.POST["user_page"]
        if "option-1" in request.POST and request.POST["option-1"]:
            user_options_ids = set(request.POST.getlist("option-1"))
            user_options = Option.objects.filter(id__in=user_options_ids)
            right_options_ids = set(
                Option.objects.filter(
                    question=user_options[0].question, right=True
                ).values_list("id", flat=True)
            )
            an = Answer.objects.create(
                attempt=at,
                question=user_options[0].question,
                right=user_options_ids == right_options_ids,
            )
            an.options.set(user_options)
    # if request.POST["user_page"] == "0":
    #     return render(request, "test_end.html", {"test": test})
    # else:
    questions = Question.objects.filter(test=test)
    paginator = Paginator(questions, 1)

    if int(page_number) > paginator.num_pages:
        return render(request, "test_end.html", {"test": test})
    else:
        page_obj = paginator.get_page(page_number)
        options = Option.objects.filter(question=page_obj.object_list)
        options_1 = Option.objects.filter(question=page_obj.object_list).first()
        l_a = set(page_obj.object_list)
        l_a_1 = list(page_obj.object_list)
        l_a_1_1 = l_a_1[0]
        options_1 = None
        form = QuestionForm(test=test.title, text=l_a_1_1.text)
        if options.filter(right=True).count() > 1:
            options_1 = Option.objects.filter(question=page_obj.object_list)
            options = None
        return render(
            request,
            "test_begin.html",
            {
                "test": test,
                "page_obj": page_obj,
                "options": options,
                "options_1": options_1,
                "form": form,
            },
        )


def result(request, pk):
    at = Attempt.objects.get(id=int(request.session.get("it")))
    answers = Question.objects.filter(test=at.test).count()
    answers_right = Answer.objects.filter(Q(attempt=at) & Q(right=True)).count()
    at.rezult = answers_right / answers * 100
    at.save()
    results = Answer.objects.filter(attempt=at)
    return render(request, "test_rezult.html", {"at": at, "results": results})
