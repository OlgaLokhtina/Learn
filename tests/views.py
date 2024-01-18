from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

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
    # at = Attempt.objects.get_or_create(user=request.user, test=test)
    if int(request.POST["user_page"]) == 1:
        at = Attempt.objects.create(user=request.user, test=test)
        request.session["it"] = str(at.id)
    else:
        at = Attempt.objects.get(id=int(request.session.get("it")))
        if "option-1" in request.POST and request.POST["option-1"]:
            ot = request.POST.getlist("option-1")
            o = Option.objects.filter(id__in=ot)
            an = Answer.objects.create(attempt=at, question=o[0].question, right=False)
            an.options.set(o)
            if an.options.filter(right=False).count() == 0:
                an.right = True
                an.save()

    if request.POST["user_page"] == "0":
        return render(request, "test_end.html", {"test": test})
    else:
        questions = Question.objects.filter(test=test)
        paginator = Paginator(questions, 1)
        request.session["num_pages"] = paginator.num_pages
        page_number = request.POST["user_page"]
        page_obj = paginator.get_page(page_number)
        options = Option.objects.filter(question=page_obj.object_list)
        options_1 = None
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
            },
        )


def result(request, pk):
    at = Attempt.objects.get(id=int(request.session.get("it")))
    results = Answer.objects.filter(attempt=at)
    answers = Question.objects.filter(test=at.test).count()
    answers_right = Answer.objects.filter(Q(attempt=at) & Q(right=True)).count()
    at.rezult = answers_right / answers * 100
    at.save()
    return render(request, "test_rezult.html", {"at": at, "results": results})
