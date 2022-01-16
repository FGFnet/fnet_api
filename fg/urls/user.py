from django.urls import path

from ..views.user import FGAPI, FGLoginAPI, FGLogoutAPI, getUserInfo

urlpatterns = [
    path('fg/', FGAPI.as_view(), name="fg_api"),
    path("login/", FGLoginAPI.as_view(), name="fg_login_api"),
    path("logout/", FGLogoutAPI.as_view(), name="fg_logout_api"),
    path("userInfo/", getUserInfo),
]