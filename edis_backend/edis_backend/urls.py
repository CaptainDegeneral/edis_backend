from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("auth/", include("auth_app.urls")),
    path("courses/", include("courses_app.urls")),
]
