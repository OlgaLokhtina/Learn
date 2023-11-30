from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import *

urlpatterns = [
    path("main/", main, name="main"),
    path("main/", include("courses.urls")),
    path("main/login/", login, name="login"),
    path("main/logout/", logout),
    path("main/profile/", get_profile, name="profile"),
    # path("main/members/", member_select, name='members'),
    path("main/members/", UserListView.as_view(), name="members"),
    path("members/<int:pk>/", MemberData.as_view(), name="member_data"),
    path("main/profile/data/", get_profile, name="get_profile"),
    path("main/profile/edit_password/", edit_password, name="edit_password"),
    # path("", include("django.contrib.auth.urls")),
    path(
        "main/profile/change_password", PasswordChange.as_view(), name="password_change"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
