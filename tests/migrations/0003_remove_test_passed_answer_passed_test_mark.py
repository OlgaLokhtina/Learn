# Generated by Django 4.2.7 on 2024-01-13 13:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0002_test_passed"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="test",
            name="passed",
        ),
        migrations.AddField(
            model_name="answer",
            name="passed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="test",
            name="mark",
            field=models.IntegerField(default=50),
            preserve_default=False,
        ),
    ]
