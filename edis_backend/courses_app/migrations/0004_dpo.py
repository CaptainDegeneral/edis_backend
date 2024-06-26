# Generated by Django 5.0.6 on 2024-06-21 11:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DPO",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type_of_education",
                    models.CharField(
                        choices=[
                            ("ПК", "Повышение квалификации"),
                            ("ПП", "Профессиональная переподготовка"),
                        ],
                        max_length=2,
                        verbose_name="Тип образования",
                    ),
                ),
                ("start_date", models.DateField(verbose_name="Дата начала")),
                ("end_date", models.DateField(verbose_name="Дата окончания")),
                (
                    "training_period",
                    models.CharField(
                        editable=False, max_length=100, verbose_name="Сроки обучения"
                    ),
                ),
                (
                    "program_name",
                    models.CharField(max_length=255, verbose_name="Название программы"),
                ),
                (
                    "training_place",
                    models.CharField(max_length=255, verbose_name="Место прохождения"),
                ),
                ("city", models.CharField(max_length=100, verbose_name="Город")),
                (
                    "certificate_number",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Номер документа",
                    ),
                ),
                (
                    "registration_number",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Регистрационный номер",
                    ),
                ),
                (
                    "issue_date",
                    models.DateField(blank=True, null=True, verbose_name="Дата выдачи"),
                ),
                (
                    "hours",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Кол-во часов"
                    ),
                ),
                (
                    "cycle_commission",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Цикловая комиссия",
                    ),
                ),
                (
                    "qualification",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Квалификация",
                    ),
                ),
                (
                    "document_type",
                    models.CharField(
                        choices=[("У", "Удостоверение"), ("Д", "Диплом")],
                        editable=False,
                        max_length=1,
                        verbose_name="Тип выданного документа",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "DPO",
                "indexes": [
                    models.Index(
                        fields=["type_of_education"], name="DPO_type_of_61acf6_idx"
                    ),
                    models.Index(fields=["user"], name="DPO_user_id_ee15a2_idx"),
                ],
            },
        ),
    ]
