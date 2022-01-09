from django.urls import path

from ..views.user import FGAPI

urlpatterns = [
    path('fg/', FGAPI.as_view(), name="fg_api")
]