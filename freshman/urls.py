from django.urls import path
from .views import *

urlpatterns = [
  path('admin/freshman/', FreshmanAPI.as_view()),
  path('admin/freshman/file', FreshmanFileUploadAPI.as_view()),
  path('admin/freshman/register', RegisterFreshmanAPI.as_view()),
  path('admin/freshman/search', searchFreshman),
  path('freshman/lc', getLCMemberList),
]