from django.urls import path, include
from .views import *

urlpatterns = [
  path('admin/freshman/', FreshmanAPI.as_view()),
  path('admin/freshman/file', FreshmanFileUploadAPI.as_view()),
  path('admin/freshman/register', registerFreshman),
  path('freshman/lc', getLCMemberList),
]