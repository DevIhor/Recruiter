# Generated by Django 4.1 on 2022-09-05 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("candidates", "0001_initial"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "title",
                    models.CharField(db_index=True, max_length=50, verbose_name="Event Type Name"),
                ),
            ],
            options={
                "verbose_name": "Event Type",
                "verbose_name_plural": "Event Types",
            },
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "title",
                    models.CharField(db_index=True, max_length=50, verbose_name="Event Title"),
                ),
                (
                    "description",
                    models.TextField(max_length=2048, verbose_name="Event Description"),
                ),
                (
                    "priority",
                    models.IntegerField(
                        choices=[
                            (None, "(Unknown)"),
                            (0, "Unspecified"),
                            (1, "Low"),
                            (2, "Moderate"),
                            (3, "High"),
                            (4, "Critical"),
                        ],
                        default=0,
                        verbose_name="Priority level",
                    ),
                ),
                ("start_time", models.DateTimeField(verbose_name="Event starts at")),
                ("end_time", models.DateTimeField(verbose_name="Event ends at")),
                (
                    "duration",
                    models.DurationField(
                        blank=True, editable=False, null=True, verbose_name="Duration"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True, verbose_name="Created at")),
                (
                    "changed_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Last updated"),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (None, "(Unspecified)"),
                            (0, "Cancelled"),
                            (1, "Active"),
                            (2, "Completed"),
                        ],
                        default=1,
                        verbose_name="Priority level",
                    ),
                ),
                (
                    "candidate_participants",
                    models.ManyToManyField(
                        blank=True,
                        related_name="events",
                        to="candidates.candidate",
                        verbose_name="Candidate Participants",
                    ),
                ),
                (
                    "event_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="events",
                        to="events.eventtype",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owner_events",
                        to="accounts.profile",
                    ),
                ),
                (
                    "staff_participants",
                    models.ManyToManyField(
                        blank=True,
                        related_name="events",
                        to="accounts.profile",
                        verbose_name="Staff Participants",
                    ),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "ordering": ("start_time",),
                "get_latest_by": ("created_at",),
            },
        ),
        migrations.AddConstraint(
            model_name="event",
            constraint=models.CheckConstraint(
                check=models.Q(("start_time__lt", models.F("end_time"))),
                name="start_before_end",
                violation_error_message="Start time should be arlier than end time.",
            ),
        ),
    ]
