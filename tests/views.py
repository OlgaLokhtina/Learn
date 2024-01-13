from django.core.paginator import Paginator
from django.shortcuts import render

from django.views.generic import ListView

from tests.models import (
    Test,
    Question,
    Option,
    Answer,
    AnswerOption,
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
    if int(request.POST["user_page"]) == 1:
        c = Answer.objects.all().count() + 1
        an = Answer(answer_name=str(c))
        request.session["it"] = str(c)
        an.user = request.user
        an.save()
    else:
        an = Answer.objects.get(answer_name=request.session.get("it"))
        ot = request.POST["option"]
        o = Option.objects.get(id=ot)
        ao = AnswerOption(option=o, answer=an)
        ao.save()

    if request.POST["user_page"] == "0":
        return render(request, "test_end.html", {"test": test})
    else:
        questions = Question.objects.filter(test=test)
        paginator = Paginator(questions, 1)
        request.session["num_pages"] = paginator.num_pages
        page_number = request.POST["user_page"]
        page_obj = paginator.get_page(page_number)
        options = Option.objects.filter(question=page_obj.object_list)
        return render(
            request,
            "test_begin.html",
            {"test": test, "page_obj": page_obj, "options": options},
        )


def result(request, pk):
    rezults = Answer.objects.get(answer_name=request.session.get("it"))
    return render(request, "test_rezult.html", {"rezults": rezults})
