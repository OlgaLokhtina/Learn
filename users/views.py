from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import View, ListView
from django.views.generic import DetailView
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db.models import Q


from .forms import UserLoginForm
from .forms import ProfileForm
from .models import User
from courses.models import Course
from .password import (
    AlphaValidator,
    MinimumLengthValidator,
    RegisterValidator,
    DigitValidator,
    SymbolValidator,
)


class Members(View):
    def get(self, request):
        mem = User.objects.order_by("last_name")
        return render(request, "members.html", {"mem": mem})


class UserListView(ListView):
    paginate_by = 2
    model = User
    template_name = "members.html"


def member_select(request):
    if request.GET.get("search-member"):
        s = request.GET.get("search-member")
        mem = User.objects.filter(
            Q(first_name__icontains=s) | Q(last_name__icontains=s)
        ).order_by("last_name")
        return render(request, "members.html", {"mem": mem, "s": s})
    else:
        mem = User.objects.order_by("last_name")
        return render(request, "members.html", {"mem": mem})


class MemberData(DetailView):
    model = User
    template_name = "memberdata.html"
    context_object_name = "member"


def get_profile(request):
    user = request.user
    if request.method == "GET":
        form = ProfileForm(instance=user)
        return render(request, "profile_edit.html", {"form": form})
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return render(request, "profile_edit.html", {"form": form, "user": user})


def login(request):
    if request.method == "POST":

        username = (request.POST)["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("main"))
        form = UserLoginForm()
        context = {"form": form}
        return render(request, "login.html", context)
    if request.method == "GET":
        form = UserLoginForm()
        context = {"form": form}
        return render(request, "login.html", context)


def edit_password(request):
    validators = [
        SymbolValidator(),
        DigitValidator(),
        MinimumLengthValidator(),
        AlphaValidator(),
        RegisterValidator(),
    ]
    help_text = []
    for v in validators:
        help_text.append(v.get_help_text())
    if request.method == "GET":
        return render(request, "edit_password.html", {"help_text": help_text})
    if request.method == "POST":
        password = request.POST["password"]
        new_password = request.POST["new_password"]
        repeat_new_password = request.POST["repeat_new_password"]
        if not request.user.check_password(password):
            message = "Не верно введен существующий пароль!"
            return render(
                request,
                "edit_password.html",
                {"help_text": help_text, "message": message},
            )
        if new_password != repeat_new_password:
            message = "Введенные пароли не совпадают!"
            return render(
                request,
                "edit_password.html",
                {"help_text": help_text, "message": message},
            )
        if new_password == request.user.password:
            message = "Новый пароль не должен быть похож на старый!"
            return render(
                request,
                "edit_password.html",
                {"help_text": help_text, "message": message},
            )
        try:
            validate_password(
                password=new_password, user=request.user, password_validators=validators
            )
        except ValidationError as error:
            return render(
                request, "edit_password.html", {"help_text": help_text, "error": error}
            )
            # return render(request, "fail.html", {"error": error, "help_text": help_text})
        request.user.set_password(new_password)
        request.user.save()
        auth.login(request, request.user)
        return render(request, "success.html")


def main(request):
    if request.user.is_authenticated:
        if request.GET.get("search"):
            symbols = request.GET.get("search")
            course_bar = Course.objects.filter(title__contains=symbols)
            return render(
                request,
                "auth.html",
                {"user": request.user, "course_bar": course_bar, "symbols": symbols},
            )
        else:
            course_bar = Course.objects.all()
            return render(
                request, "auth.html", {"user": request.user, "course_bar": course_bar}
            )
    form = UserLoginForm()
    context = {"form": form}
    return render(request, "login.html", context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main"))


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy("profile")
    template_name = "password_change_form.html"
