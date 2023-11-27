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
    views = CourseView.objects.all()

    workbook = xlsxwriter.Workbook('static/courses/stat.xlsx')
    worksheet = workbook.add_worksheet('Статистика просмотров')
    bold = workbook.add_format({'bold': True})
    cell_format = workbook.add_format({'align': 'center_across'})

    worksheet.write('A1', 'Пользователь', cell_format)
    worksheet.write('B1', 'Наименование курса', bold)
    worksheet.write('C1', 'Время посещения', bold)

    row = 1
    col = 0

    for v in views:
        worksheet.write(row, col, v.user.first_name)
        worksheet.write(row, col + 1, v.course.title)
        worksheet.write(row, col + 2, str(v.date))
        row += 1

    workbook.close()
    return render(request, "load.html")

def listing(request):
    course_name = None
    u_name = None
    if request.GET.get('course_name'):
        course_name = request.GET.get('course_name')
        view_list = CourseView.objects.filter(course__title=course_name)
    else:
        view_list = CourseView.objects.all()
    if request.GET.get("user_name"):
        u_name = request.GET.get("user_name")
        view_list = view_list.filter(user__username=u_name)
    else:
        view_list = CourseView.objects.all()


    paginator = Paginator(view_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    user_list = User.objects.all()
    course_list = Course.objects.all()
    return render(request, "statistic.html", {"page_obj": page_obj, "views": view_list, "user_list": user_list, "course_list": course_list, "course_name": course_name, "u_name": u_name})


