# Generated by Django 4.1 on 2022-09-11 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="curriculumvitae",
            name="changed_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Last updated"),
        ),
        migrations.AlterField(
            model_name="curriculumvitae",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
        ),
    ]
