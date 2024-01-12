import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyLearn.settings")
django.setup()

from django.db import transaction
from courses.models import Course, TypeBlock, Block
from users.models import User
from tests.models import Test, Question, Option

def create_users():
    user = User.objects.create(username="admin", is_active=True, is_superuser=True, is_staff=True)
    user.set_password("password")
    user.save()


def create_courses():
    course = Course.objects.create(title="Course 1", order=1)
    html_type = TypeBlock.objects.create(name="html")
    image_type = TypeBlock.objects.create(name="image")
    Block.objects.bulk_create([
        Block(course=course, order=1, type=html_type, text="html text"),
        Block(course=course, order=2, type=image_type, image="/path/to/image.jpg"),
    ])


def create_tests():
    test = Test.objects.create(title="Test 1")
    questions = Question.objects.bulk_create([
        Question(test=test, text="yes/no?"),
        Question(test=test, text="yes/no?"),
    ])
    options = []
    for q in questions:
        options.extend([
            Option(question=q, text="yes", right=True),
            Option(question=q, text="no", right=False),
        ])
    Option.objects.bulk_create(options)


@transaction.atomic()
def main():
    create_users()
    create_courses()
    create_tests()


if __name__ == "__main__":
    main()
