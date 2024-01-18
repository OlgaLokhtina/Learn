from django.db import models
from django.utils import timezone
import datetime
from users.models import User

# Create your models here.


class Test(models.Model):
    title = models.CharField(max_length=50)
    preview = models.ImageField(upload_to="courses")
    description = models.TextField()
    mark = models.FloatField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Question(models.Model):
    test = models.ForeignKey(
        Test, default=None, null=True, on_delete=models.SET_DEFAULT
    )
    text = models.TextField()

    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(
        Question, default=None, null=True, on_delete=models.SET_DEFAULT
    )
    text = models.TextField()
    right = models.BooleanField(default=None)

    def __str__(self):
        return self.text


class Attempt(models.Model):
    test = models.ForeignKey(
        Test, default=None, null=True, on_delete=models.SET_DEFAULT
    )
    user = models.ForeignKey(
        User, default=None, null=True, on_delete=models.SET_DEFAULT
    )
    start = models.DateTimeField(default=timezone.now)
    finish = models.DateTimeField(default=timezone.now)
    rezult = models.FloatField(default=0)


class Answer(models.Model):
    attempt = models.ForeignKey(
        Attempt, default=None, null=True, on_delete=models.SET_DEFAULT
    )
    question = models.ForeignKey(
        Question, default=None, null=True, on_delete=models.SET_DEFAULT
    )
    right = models.BooleanField(default=None)
    options = models.ManyToManyField(Option)


# class AnswerOption(models.Model):
#     answer = models.ForeignKey(
#         Answer, default=None, null=True, on_delete=models.SET_DEFAULT
#     )
#     option = models.ForeignKey(
#         Option, default=None, null=True, on_delete=models.SET_DEFAULT
#     )
