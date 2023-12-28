from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import *


urlpatterns = [
    path("course/<int:id>/", course, name="course"),
    path("statistic/", listing, name="listing"),
    path("statistic/load/", statistic, name="statistic"),
    path("test/", TestView.as_view(), name="test_view"),
    path("test/<int:pk>/", test, name="test"),
    path("test/<int:pk>/attempt/", test_attempt, name="test_attempt"),
    path("test/<int:pk>/result/", result, name="result"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
