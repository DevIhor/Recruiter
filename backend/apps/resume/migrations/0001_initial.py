# Generated by Django 4.1 on 2022-09-11 07:47

import apps.resume.models
import apps.resume.storages
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("candidates", "0002_candidate_vacancy"),
        ("vacancies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CurriculumVitae",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        storage=apps.resume.storages.OverwriteStorage(),
                        upload_to=apps.resume.models.generate_file_path,
                        verbose_name="CV file",
                    ),
                ),
                (
                    "content",
                    models.TextField(blank=True, max_length=2048, verbose_name="CV content"),
                ),
                (
                    "processed_by_tesseract",
                    models.BooleanField(default=False, verbose_name="Processed by tesseract"),
                ),
                ("created_at", models.DateTimeField(auto_now=True, verbose_name="Created at")),
                (
                    "changed_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Last updated"),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cv_owner",
                        to="candidates.candidate",
                        verbose_name="CV owner",
                    ),
                ),
                (
                    "vacancy",
                    models.ManyToManyField(
                        blank=True,
                        related_name="cv_vacancies",
                        to="vacancies.vacancy",
                        verbose_name="Vacancies",
                    ),
                ),
            ],
            options={
                "ordering": ("-id",),
            },
        ),
    ]
