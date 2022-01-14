from django.urls import path
from .views import *

urlpatterns = [
    path('lc/', LCAPI.as_view(), name="lc_api"),
]