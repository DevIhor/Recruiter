# Generated by Django 4.1 on 2022-09-03 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="duration",
            field=models.DurationField(blank=True, editable=False, verbose_name="End time"),
        ),
    ]