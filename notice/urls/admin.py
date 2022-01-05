from django.urls import path

from notice.views.admin import NoticeAdminAPI


urlpatterns = [
    path("notice/", NoticeAdminAPI.as_view(), name="notice_admin_api"),
]
