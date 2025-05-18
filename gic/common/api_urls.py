from django.contrib import admin
from django.urls import path
from common.api_views import FileUploadViewset

urlpatterns = [
    path(
        "file-upload/",
        FileUploadViewset.as_view({"post": "create"}),
        name="file_upload",
    ),
]
