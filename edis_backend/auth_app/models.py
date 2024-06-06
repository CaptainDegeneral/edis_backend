from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, last_name, first_name, email, password=None):
        """Создает и сохраняет нового пользователя с указанными фамилией, именем и электронной почтой."""

        if not last_name:
            raise ValueError("Пользователь должен иметь фамилию.")
        if not first_name:
            raise ValueError("Пользователь должен иметь имя.")
        if not email:
            raise ValueError("Пользователь должен иметь адрес электронной почты.")

        user = self.model(
            last_name=last_name,
            first_name=first_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, last_name, first_name, email, password):
        """Создает и сохраняет суперпользователя с указанными фамилией, именем и электронной почтой."""

        if not last_name:
            raise ValueError("Суперпользователь должен иметь фамилию.")
        if not first_name:
            raise ValueError("Суперпользователь должен иметь имя.")
        if not email:
            raise ValueError("Суперпользователь должен иметь адрес электронной почты.")
        if not password:
            raise ValueError("Суперпользователь должен иметь пароль.")

        user = self.create_user(last_name, first_name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Пользовательская модель пользователя, поддерживающая использование электронной почты вместо имени пользователя."""

    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=255)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["last_name", "first_name"]

    def __str__(self):
        """Возвращает строковое представление пользователя в виде его email-адреса."""
        return self.email

    def tokens(self):
        """Возвращает токены доступа и обновления для данного пользователя."""
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        return f"{self.last_name} {self.first_name}"

    def get_short_name(self):
        """Возвращает сокращенное имя пользователя."""
        return f"{self.last_name} {self.first_name[0]}."

    class Meta:
        db_table = "user"
