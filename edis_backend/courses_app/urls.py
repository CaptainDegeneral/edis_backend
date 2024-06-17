from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
    path("", CourseListCreateView.as_view(), name="course-list-create"),
    path("<int:pk>", CourseDetailView.as_view(), name="course-detail"),
    path("user/current", UserCoursesView.as_view(), name="user-courses"),
    path("user/<int:user_id>", UserCoursesView.as_view(), name="user-courses-specific"),
]
