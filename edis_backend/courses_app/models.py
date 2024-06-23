from django.db import models
from auth_app.models import User


class DPO(models.Model):
    EDUCATION_TYPES = [
        ("ПК", "Повышение квалификации"),
        ("ПП", "Профессиональная переподготовка"),
    ]

    DOCUMENT_TYPES = [("У", "Удостоверение"), ("Д", "Диплом")]

    type_of_education = models.CharField(
        max_length=2, choices=EDUCATION_TYPES, verbose_name="Тип образования"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    training_period = models.CharField(
        max_length=100, verbose_name="Сроки обучения", editable=False
    )
    program_name = models.CharField(max_length=255, verbose_name="Название программы")
    training_place = models.CharField(max_length=255, verbose_name="Место прохождения")
    city = models.CharField(max_length=100, verbose_name="Город")
    certificate_number = models.CharField(
        max_length=50, verbose_name="Номер документа", null=True, blank=True
    )
    registration_number = models.CharField(
        max_length=50, verbose_name="Регистрационный номер", null=True, blank=True
    )
    issue_date = models.DateField(verbose_name="Дата выдачи", null=True, blank=True)
    hours = models.IntegerField(verbose_name="Кол-во часов", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle_commission = models.CharField(
        max_length=100, verbose_name="Цикловая комиссия", null=True, blank=True
    )
    qualification = models.CharField(
        max_length=100, verbose_name="Квалификация", null=True, blank=True
    )
    document_type = models.CharField(
        max_length=1,
        choices=DOCUMENT_TYPES,
        verbose_name="Тип выданного документа",
        editable=False,
    )
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        db_table = "DPO"
        indexes = [
            models.Index(fields=["type_of_education"]),
            models.Index(fields=["user"]),
        ]

    def calculate_training_period(self):
        return f"{self.start_date.strftime('%d.%m.%Y')}-{self.end_date.strftime('%d.%m.%Y')}"

    def save(self, *args, **kwargs):
        self.training_period = self.calculate_training_period()

        if self.type_of_education == "ПК":
            self.document_type = "У"
        elif self.type_of_education == "ПП":
            self.document_type = "Д"
        else:
            self.document_type = "Н"

        super().save(*args, **kwargs)

    def formatted_course_info(self):
        education_type = dict(self.EDUCATION_TYPES).get(self.type_of_education, "")
        document_type = "Удостоверение" if self.document_type == "У" else "Диплом"
        issue_date = self.issue_date.strftime("%d.%m.%Y") if self.issue_date else "N/A"
        return (
            f"{self.training_period}, Вид образования: {education_type}, Наименование курса: {self.program_name}, "
            f"{self.hours} ч., Вид документа: {document_type}, Номер: {self.certificate_number}, "
            f"Рег. номер: {self.registration_number}, Дата выдачи: {issue_date}, "
            f"Выдан: {self.training_place}, г. {self.city}."
        )

    def __str__(self):
        return f"{self.program_name} ({self.user.last_name} {self.user.first_name[0]}.)"
