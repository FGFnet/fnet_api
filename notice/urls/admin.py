from django.urls import path

from ..views.admin import CommentAdminAPI, NoticeAdminAPI


urlpatterns = [
    path("notice/", NoticeAdminAPI.as_view(), name="notice_admin_api"),
    path("notice/comment/", CommentAdminAPI.as_view(), name="comment_admin_api"),
]
