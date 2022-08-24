# Generated by Django 4.1 on 2022-08-24 18:20

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Candidate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=50, verbose_name="Firstname")),
                ("surname", models.CharField(db_index=True, max_length=50, verbose_name="Surname")),
                (
                    "date_of_birth",
                    models.DateField(blank=True, null=True, verbose_name="Birth date"),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                        default="O",
                        max_length=1,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        db_index=True,
                        max_length=128,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, db_index=True, max_length=100, verbose_name="Email address"
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, max_length=255, null=True, verbose_name="Additional info"
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Last update")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
            ],
            options={
                "ordering": ("surname", "name"),
            },
        ),
    ]
