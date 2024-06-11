from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
    path("", CourseListCreateView.as_view(), name="course-list-create"),
    path("<int:pk>", CourseDetailView.as_view(), name="course-detail"),
]
