# Generated by Django 5.0.6 on 2024-06-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0005_delete_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpo',
            name='is_processed',
            field=models.BooleanField(default=False, verbose_name='Обработано'),
        ),
    ]
