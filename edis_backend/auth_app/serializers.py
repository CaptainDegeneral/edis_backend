from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from courses_app.models import DPO

from .models import *
from .utils import *


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя в системе."""

    email = serializers.EmailField(max_length=255, min_length=4)
    password = serializers.CharField(max_length=255, min_length=9, write_only=True)

    class Meta:
        model = User
        fields = ["last_name", "first_name", "email", "password"]

    def validate(self, attrs):
        """Проверяет входные данные перед созданием новой учетной записи пользователя."""

        email = attrs.get("email", "")

        if not email:
            raise serializers.ValidationError(
                "Пожалуйста, укажите адрес электронной почты для создания новой учетной записи."
            )

        if User.objects.filter(email=email, is_verified=True).exists():
            raise serializers.ValidationError(
                "Пользователь с этим адресом электронной почты уже существует."
            )

        if User.objects.filter(email=email, is_verified=False).exists():
            User.objects.filter(email=email, is_verified=False).delete()

        last_name = attrs.get("last_name", "")

        if not last_name:
            raise serializers.ValidationError(
                "Пожалуйста, укажите фамилию для создания новой учетной записи."
            )

        if len(last_name) < 2:
            raise serializers.ValidationError(
                "Фамилия не должно быть короче 2 символов."
            )

        if len(last_name) > 50:
            raise serializers.ValidationError(
                "Фамилия не должна быть длиннее 50 символов."
            )

        if not last_name.isalpha():
            raise serializers.ValidationError("Фамилия должна содержать только буквы.")

        first_name = attrs.get("first_name", "")

        if not first_name:
            raise serializers.ValidationError(
                "Пожалуйста, укажите имя для создания новой учетной записи."
            )

        if len(first_name) < 2:
            raise serializers.ValidationError("Имя не должно быть короче 2 символов.")

        if len(first_name) > 50:
            raise serializers.ValidationError("Имя не должно быть длиннее 50 символов.")

        if not first_name.isalpha():
            raise serializers.ValidationError("Имя должно содержать только буквы.")

        return super().validate(attrs)

    def create(self, validated_data):
        """Создает и сохраняет нового пользователя с указанными фамилией, именем и электронной почтой."""

        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    """Сериализатор для подтверждения email пользователя при регистрации."""

    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class SignInSerializer(serializers.ModelSerializer):
    """Сериализатор для входа в систему."""

    email = serializers.EmailField(max_length=255, min_length=4)
    password = serializers.CharField(max_length=255, min_length=9, write_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "is_staff"]

    def validate(self, attrs):
        """Проверяет входные данные перед входом в систему."""

        email = attrs.get("email", "")
        password = attrs.get("password", "")

        if not email:
            raise serializers.ValidationError(
                "Пожалуйста, укажите ваш адрес электронной почты для входа в систему."
            )

        user = User.objects.filter(email=email).first()

        if user is None or not user.is_verified:
            raise serializers.ValidationError(
                "Пользователь с этим адресом электронной почты не зарегистрирован."
            )

        if not auth.authenticate(email=email, password=password):
            raise serializers.ValidationError(
                "Неверный адрес электронной почты или пароль."
            )

        user.last_login = datetime.now().replace(second=0, microsecond=0)
        user.save(update_fields=["last_login"])

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "tokens": user.tokens(),
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    """Сериализатор для запроса сброса пароля."""

    email = serializers.EmailField(min_length=4, max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        """Проверяет входные данные перед запросом сброса пароля."""

        email = attrs.get("email", "")

        if not email:
            raise serializers.ValidationError(
                "Пожалуйста, укажите ваш адрес электронной почты для сброса пароля."
            )

        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    """Сериализатор для установки нового пароля."""

    password = serializers.CharField(min_length=9, max_length=255, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "uidb64", "token"]

    def validate(self, attrs):
        """Проверяет входные данные перед установкой нового пароля."""

        try:
            password = attrs.get("password")
            uidb64 = attrs.get("uidb64")
            token = attrs.get("token")

            user = User.objects.get(id=force_str(urlsafe_base64_decode(uidb64)))

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    "Ссылка для сброса пароля недействительна.", code=401
                )

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed(
                "Ссылка для сброса пароля недействительна.", code=401
            )


class SignOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "invalid_token": ("Token is expired or invalid."),
    }

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("invalid_token")


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(required=False)
    is_verified = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
            "is_verified",
        )

    def validate_email(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)

        if "is_staff" in validated_data:
            if self.context["request"].user.is_staff:
                instance.is_staff = validated_data["is_staff"]
            else:
                raise serializers.ValidationError(
                    "Только персонал может обновлять статус персонала."
                )

        if "is_verified" in validated_data:
            if self.context["request"].user.is_staff:
                instance.is_verified = validated_data["is_verified"]
            else:
                raise serializers.ValidationError(
                    "Только персонал может обновлять статус проверки."
                )

        instance.save()

        updated_user = {
            "id": instance.id,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "is_staff": instance.is_staff,
            "is_verified": instance.is_verified,
        }
        return updated_user


class UserListSerializer(serializers.ModelSerializer):
    pp = serializers.SerializerMethodField()
    pk = serializers.SerializerMethodField()
    up = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_verified",
            "pp",
            "pk",
            "up",
        )

    def get_pp(self, obj):
        return DPO.objects.filter(user=obj, type_of_education="ПП").count()

    def get_pk(self, obj):
        return DPO.objects.filter(user=obj, type_of_education="ПК").count()

    def get_up(self, obj):
        return DPO.objects.filter(user=obj, processed=False).count()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "is_staff", "is_verified")


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            is_staff=validated_data.get("is_staff", False),
            is_verified=True,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "last_name", "first_name", "email", "is_staff", "is_verified")
