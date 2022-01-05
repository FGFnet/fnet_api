from django.urls import path

from ..views.user import NoticeAPI, NoticeCommentAPI


urlpatterns = [
    path("notice/", NoticeAPI.as_view(), name="notice_api"),
    path("notice/comment/", NoticeCommentAPI.as_view(), name="notice_comment_api"),
]
