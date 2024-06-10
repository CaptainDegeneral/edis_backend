from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path("signup", SignUpAPIView.as_view(), name="signup"),
    path("signin", SignInAPIView.as_view(), name="signin"),
    path("signout", SignOutAPIView.as_view(), name="signout"),
    path("verify-email", VerifyEmailAPIView.as_view(), name="verify-email"),
    path("token-refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "password-reset", ResetPasswordAPIView.as_view(), name="password-reset-request"
    ),
    path(
        "password-reset/<uidb64>/<token>",
        PasswordTokenCheckAPIView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
]
