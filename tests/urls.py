from django.urls import path, include

from .views import *


urlpatterns = [
    path("", TestView.as_view(), name="test_view"),
    path("<int:pk>/", test, name="test"),
    path("<int:pk>/attempt/", test_attempt, name="test_attempt"),
    path("<int:pk>/result/", result, name="result"),
]
