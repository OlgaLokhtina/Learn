# Generated by Django 4.2.7 on 2024-01-16 10:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0004_remove_answer_answer_name_remove_answer_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="answer",
            name="options",
        ),
        migrations.DeleteModel(
            name="AnswerOption",
        ),
    ]
