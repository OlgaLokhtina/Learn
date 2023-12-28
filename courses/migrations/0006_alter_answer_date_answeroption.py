# Generated by Django 4.2.7 on 2023-12-21 09:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0005_test_alter_block_options_alter_course_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 12, 21, 9, 57, 36, 66074, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.CreateModel(
            name="AnswerOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "answer",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="courses.answer",
                    ),
                ),
                (
                    "option",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="courses.option",
                    ),
                ),
            ],
        ),
    ]
