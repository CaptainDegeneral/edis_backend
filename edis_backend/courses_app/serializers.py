from rest_framework import serializers

from .models import *


class CourseSerializerWithUser(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "course_type",
            "course_name",
            "institution",
            "city",
            "start_date",
            "end_date",
            "hours",
            "document_type",
            "document_number",
            "registration_number",
            "issue_date",
            "user",
        ]

    def get_user(self, obj):
        request = self.context.get("request")
        if request and request.user.is_staff:
            return {
                "id": obj.user.id,
                "email": obj.user.email,
                "first_name": obj.user.first_name,
                "last_name": obj.user.last_name,
            }
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        if request and not request.user.is_staff:
            representation.pop("user", None)
        return representation


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
