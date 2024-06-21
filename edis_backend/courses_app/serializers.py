from rest_framework import serializers

from .models import *


class CourseSerializerWithUser(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    cycle_commission = serializers.CharField(
        max_length=100, allow_blank=True, required=True
    )
    qualification = serializers.CharField(
        max_length=100, allow_blank=True, required=False
    )

    class Meta:
        model = DPO
        fields = [
            "id",
            "type_of_education",
            "start_date",
            "end_date",
            "training_period",
            "program_name",
            "training_place",
            "city",
            "certificate_number",
            "registration_number",
            "issue_date",
            "hours",
            "cycle_commission",
            "qualification",
            "document_type",
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
        representation["cycle_commission"] = instance.cycle_commission
        representation["qualification"] = (
            instance.qualification if instance.qualification else None
        )
        return representation


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DPO
        fields = "__all__"
