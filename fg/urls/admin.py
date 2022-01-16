from django.urls import path

from ..views.admin import FGAPI, FGFileUploadAPI, searchFG

urlpatterns = [
    path('fg/', FGAPI.as_view(), name="fg_admin_api"),
    path('fg/file', FGFileUploadAPI.as_view(), name="fg_file_upload_admin_api"),
    path('fg/search/', searchFG, name="search_fg_by_name"),
]