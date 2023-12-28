from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
import xlsxwriter
from django.views.generic import ListView

from courses.models import (
    Course,
    Block,
    CourseView,
    Test,
    Question,
    Option,
    Answer,
    AnswerOption,
)
from users.models import User


def course(request, id):
    user_in = request.user
    c = Course.objects.get(id=id)
    b = Block.objects.filter(course=c).order_by("order")
    course_view = CourseView(user=user_in, course=c)
    course_view.save()
    return render(request, "course.html", {"b": b, "c": c})


def statistic(request):
    view_list = CourseView.objects.all()
    course_name = request.GET.get("course_name")
    u_name = request.GET.get("user_name")
    if course_name != "all":
        view_list = view_list.filter(course__title=course_name)
    if u_name != "all":
        view_list = view_list.filter(user__username=u_name)

    workbook = xlsxwriter.Workbook("media/stat.xlsx", {"remove_timezone": True})
    worksheet = workbook.add_worksheet("Статистика просмотров")
    bold = workbook.add_format({"bold": True})
    cell_format = workbook.add_format({"align": "center_across"})

    worksheet.write("A1", "Пользователь", bold)
    worksheet.write("B1", "Наименование курса", bold)
    worksheet.write("C1", "Время посещения", bold)

    cell_format01 = workbook.add_format({"num_format": "d mmmm yyyy"})
    worksheet.set_column(2, 2, 20, cell_format01)

    correct_list = view_list.values_list("user__first_name", "course__title", "date")

    for row_num, v in enumerate(correct_list):
        for col_num, s in enumerate(v):
            worksheet.write(row_num + 1, col_num, s)

    workbook.close()
    return HttpResponseRedirect(redirect_to="/media/stat.xlsx")


def listing(request):
    view_list = CourseView.objects.all()
    course_name = request.GET.get("course_name")
    u_name = request.GET.get("user_name")
    if course_name != "all":
        view_list = view_list.filter(course__title=course_name)
    if u_name != "all":
        view_list = view_list.filter(user__username=u_name)
    paginator = Paginator(view_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    user_list = User.objects.all().order_by("username")
    course_list = Course.objects.all().order_by("title")
    return render(
        request,
        "statistic.html",
        {
            "page_obj": page_obj,
            "view_list": view_list,
            "user_list": user_list,
            "course_list": course_list,
            "course_name": course_name,
            "u_name": u_name,
        },
    )


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
        o = Option.objects.get(text=ot)
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
