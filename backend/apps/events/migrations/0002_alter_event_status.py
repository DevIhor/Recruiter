# Generated by Django 4.1 on 2022-09-11 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="status",
            field=models.IntegerField(
                choices=[
                    (None, "(Unspecified)"),
                    (0, "Cancelled"),
                    (1, "Active"),
                    (2, "Completed"),
                ],
                default=1,
                verbose_name="Status",
            ),
        ),
    ]
