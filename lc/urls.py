from django.urls import path
from .views import LcAPI

urlpatterns = [
    path('lc/', LcAPI.as_view(), name="lc_api"),
]