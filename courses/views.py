from django.shortcuts import render
import xlsxwriter
from django.core.paginator import Paginator


from courses.models import Course, Block, CourseView
from users.models import User

# Create your views here.


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

    workbook = xlsxwriter.Workbook("media/stat.xlsx")
    worksheet = workbook.add_worksheet("Статистика просмотров")
    bold = workbook.add_format({"bold": True})
    cell_format = workbook.add_format({"align": "center_across"})

    worksheet.write("A1", "Пользователь", cell_format)
    worksheet.write("B1", "Наименование курса", bold)
    worksheet.write("C1", "Время посещения", bold)

    row = 1
    col = 0

    for v in view_list:
        worksheet.write(row, col, v.user.first_name)
        worksheet.write(row, col + 1, v.course.title)
        worksheet.write(row, col + 2, str(v.date))
        row += 1

    workbook.close()
    return render(request, "load.html")


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
    # if request.method == "POST":
    #     view_list = request.GET.get("list")
    #
    #     workbook = xlsxwriter.Workbook("media/stat.xlsx")
    #     worksheet = workbook.add_worksheet("Статистика просмотров")
    #     bold = workbook.add_format({"bold": True})
    #     cell_format = workbook.add_format({"align": "center_across"})
    #
    #     worksheet.write("A1", "Пользователь", cell_format)
    #     worksheet.write("B1", "Наименование курса", bold)
    #     worksheet.write("C1", "Время посещения", bold)
    #
    #     row = 1
    #     col = 0
    #
    #     for v in view_list:
    #         worksheet.write(row, col, v.user.first_name)
    #         worksheet.write(row, col + 1, v.course.title)
    #         worksheet.write(row, col + 2, str(v.date))
    #         row += 1
    #
    #     workbook.close()
    #     return render(request, "load.html")
