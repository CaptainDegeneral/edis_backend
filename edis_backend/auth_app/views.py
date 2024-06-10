from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import (
    smart_str,
    force_str,
    force_bytes,
    smart_bytes,
    DjangoUnicodeDecodeError,
)

import jwt
import os

from .serializers import *
from .models import *
from .utils import *

from dotenv import load_dotenv

load_dotenv()


class SignUpAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data

            user = User.objects.get(email=user_data["email"])
            token = RefreshToken.for_user(user).access_token

            frontend_url = os.getenv("FRONTEND_DOMAIN")
            absolute_url = f"{frontend_url}/verify-email?token={str(token)}"

            email_data = {
                "email_body": Util.get_verification_email_body(
                    user.first_name, absolute_url
                ),
                "email_subject": "Подтверждение регистрации на платформе EDIS",
                "email_to": user.email,
            }

            Util.send_email(email_data)

            return Response(
                {"success": True, "data": user_data}, status=status.HTTP_201_CREATED
            )
        except ValidationError as err:
            error_dict = {}
            if hasattr(err, "detail"):
                for field, errors in err.detail.items():
                    error_dict[field] = errors[0] if errors else ""
            else:
                error_dict["non_field_errors"] = str(err)

            return Response(
                {"success": False, "error": error_dict},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyEmailAPIView(views.APIView):

    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response(
                    {
                        "success": True,
                        "message": "Адрес электронной почты успешно подтвержден.",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Ссылка для подтверждения адреса электронной почты недействительна.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except jwt.ExpiredSignatureError as err:
            return Response(
                {"success": False, "error": str(err)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError as err:
            return Response(
                {"success": False, "error": str(err)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignInAPIView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return Response(
                {"success": True, "data": serializer.validated_data},
                status=status.HTTP_200_OK,
            )
        except ValidationError as err:
            error_dict = {}
            if hasattr(err, "detail"):
                for field, errors in err.detail.items():
                    error_dict[field] = errors[0] if errors else ""
            else:
                error_dict["non_field_errors"] = str(err)

            return Response(
                {"success": False, "error": error_dict},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignOutAPIView(generics.GenericAPIView):

    def post(self, request):
        pass


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            email = request.data["email"]

            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)

                frontend_url = os.getenv("FRONTEND_DOMAIN")
                absolute_url = f"{frontend_url}/password-reset/{uidb64}/{token}/"

                email_data = {
                    "email_body": Util.get_password_reset_email_body(
                        user.first_name, absolute_url
                    ),
                    "email_subject": "Сброс пароля на платформе EDIS",
                    "email_to": user.email,
                }
                Util.send_email(email_data)

            return Response(
                {"success": True},
                status=status.HTTP_200_OK,
            )

        except ValidationError as err:
            error_dict = {}
            if hasattr(err, "detail"):
                for field, errors in err.detail.items():
                    error_dict[field] = errors[0] if errors else ""
            else:
                error_dict["non_field_errors"] = str(err)

            return Response(
                {"success": False, "error": error_dict},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user = User.objects.get(id=smart_str(urlsafe_base64_decode(uidb64)))
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Ссылка для сброса пароля недействительна."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response(
                {"success": True, "uidb64": uidb64, "token": token},
                status=status.HTTP_200_OK,
            )
        except Exception as err:
            error_dict = {}
            if hasattr(err, "detail"):
                for field, errors in err.detail.items():
                    error_dict[field] = errors[0] if errors else ""
            else:
                error_dict["non_field_errors"] = str(err)

            return Response(
                {"success": False, "error": error_dict},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            return Response({"success": True}, status=status.HTTP_200_OK)

        except ValidationError as err:
            error_dict = {}
            if hasattr(err, "detail"):
                for field, errors in err.detail.items():
                    error_dict[field] = errors[0] if errors else ""
            else:
                error_dict["non_field_errors"] = str(err)

            return Response(
                {"success": False, "error": error_dict},
                status=status.HTTP_400_BAD_REQUEST,
            )
