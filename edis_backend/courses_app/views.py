from rest_framework import generics, status, filters, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Course
from .serializers import *
from .permissions import IsAuthorOrStaff


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializerWithUser
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user", "start_date", "end_date"]
    ordering_fields = ["start_date", "end_date"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializerWithUser
    permission_classes = [IsAuthenticated, IsAuthorOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        response = {"detail": "Удаление курсов запрещено."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class UserCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if "user_id" in self.kwargs:
            if not user.is_staff and user.id != int(self.kwargs["user_id"]):
                raise PermissionDenied(
                    "You do not have permission to access these courses."
                )
            queryset = Course.objects.filter(user_id=self.kwargs["user_id"]).order_by(
                "-start_date"
            )
        else:
            queryset = Course.objects.filter(user=user).order_by("-start_date")
        return queryset
