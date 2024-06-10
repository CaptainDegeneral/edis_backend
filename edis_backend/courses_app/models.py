from django.db import models
from auth_app.models import User


class Course(models.Model):
    COURSE_TYPES = [
        ("ПК", "Повышение квалификации"),
        ("ПП", "Профессиональная переподготовка"),
        ("ДР", "Другое"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_type = models.CharField(
        max_length=2, choices=COURSE_TYPES, verbose_name="Тип курса"
    )
    course_name = models.CharField(max_length=255, verbose_name="Название курса")
    institution = models.CharField(max_length=255, verbose_name="Учреждение")
    city = models.CharField(max_length=100, verbose_name="Город")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    hours = models.PositiveIntegerField(verbose_name="Количество часов")
    document_type = models.CharField(max_length=100, verbose_name="Тип документа")
    document_number = models.CharField(max_length=100, verbose_name="Номер документа")
    registration_number = models.CharField(
        max_length=100, verbose_name="Регистрационный номер"
    )
    issue_date = models.DateField(verbose_name="Дата выдачи")

    def __str__(self):
        return f"{self.course_name} ({self.user.last_name} {self.user.first_name[0]}.)"

    class Meta:
        db_table = "course"
        indexes = [
            models.Index(fields=["course_type"]),
            models.Index(fields=["user"]),
        ]
