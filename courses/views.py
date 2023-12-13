from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
import xlsxwriter

from courses.models import Course, Block, CourseView
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

    worksheet.write("A1", "Пользователь", bold, cell_format)
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
