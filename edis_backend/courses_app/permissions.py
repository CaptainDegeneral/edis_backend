from rest_framework.permissions import BasePermission


class IsAuthorOrStaff(BasePermission):
    """
    Разрешает доступ только авторам записи или пользователям со статусом персонала.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешает чтение всем пользователям
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        # Разрешает изменение только авторам записи или пользователям со статусом персонала
        return obj.user == request.user or request.user.is_staff
