from django.urls import path

from ..views.user import NoticeAPI


urlpatterns = [
    path("notice/", NoticeAPI.as_view(), name="notice_api"),
]
