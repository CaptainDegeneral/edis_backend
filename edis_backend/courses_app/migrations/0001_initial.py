# Generated by Django 5.0.6 on 2024-06-10 15:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_type', models.CharField(choices=[('ПК', 'Повышение квалификации'), ('ПП', 'Профессиональная переподготовка'), ('ДР', 'Другое')], max_length=2, verbose_name='Тип курса')),
                ('course_name', models.CharField(max_length=255, verbose_name='Название курса')),
                ('institution', models.CharField(max_length=255, verbose_name='Учреждение')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('hours', models.PositiveIntegerField(verbose_name='Количество часов')),
                ('document_type', models.CharField(max_length=100, verbose_name='Тип документа')),
                ('document_number', models.CharField(max_length=100, verbose_name='Номер документа')),
                ('registration_number', models.CharField(max_length=100, verbose_name='Регистрационный номер')),
                ('issue_date', models.DateField(verbose_name='Дата выдачи')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course',
                'indexes': [models.Index(fields=['course_type'], name='course_course__9e4d8d_idx'), models.Index(fields=['user'], name='course_user_id_ee10f8_idx')],
            },
        ),
    ]
