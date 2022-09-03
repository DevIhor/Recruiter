from base.models import EventStatusChoices, PriorityChoices
from django.db import models
from django.utils.translation import gettext_lazy as _


class EventType(models.Model):
    """
    This class represents an event type. It is similar to categories.

    Attributes
    ----------
    title : str
        title of the Event Type
    events : list
        provides all the events of this type (through the M2MK)

    """

    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")

    title = models.CharField(
        _("Event Type Name"),
        max_length=50,
        db_index=True,
    )

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"<EventType (id={self.id}) - {self.title}>"


class Event(models.Model):
    """
    This class represents an Event which can be held by Recruiters (or generally
    by staff members), where they can invite other staff members and candidates.

    Attributes
    ----------
    title : str
        a title of the event
    description : str
        a description of the event
    event_type : EventType
        a type of the event, which is defined by EventType model
    priority : int
        a priority of the event, defined by enum PriorityChoices
    owner : Profile
        an owner of the event (aka contact person)
    staff_participants : Profile
        staff members that will (or planning to) participate in the event
    candidate_participants : Candidate
        candidates that will (or planning to) participate in the event
    start_time : datetime
        start time of the event
    end_time : datetime
        end time of the event
    duration : timedelta
        duration of the event, it is being calculated on creation/update
    created_at : datetime
        time of creation of the event
    changed_at : datetime
        last time the event was changed
    status : int
        shows status of the event, enum EventStatusChoices
    is_active : bool
        returns True if event is active
    is_completed : bool
        returns True if event is COMPLETED
    cancelled : bool
        returns True if event is CANCELLED

    Methods
    ----------
    mark_as_active():
        marks event as ACTIVE
    mark_as_completed():
        marks event as COMPLETED
    mark_as_cancelled():
        marks event as CANCELLED

    TODO
    ----------
    * After adding Celery, we can automatically put events to COMPLETED
    if time is up...
    * We can do an automatic email notification if the event was cancelled
    (Celery + signals)

    """

    class Meta:
        ordering = ("start_time",)
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        get_latest_by = ("created_at",)

        constraints = (
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F("end_time")),
                name="start_before_end",
                violation_error_message="Start time should be arlier than end time.",
            ),
        )

    title = models.CharField(
        _("Event Title"),
        max_length=50,
        db_index=True,
    )
    description = models.TextField(
        _("Event Description"),
        max_length=2048,
    )
    event_type = models.ForeignKey(
        to=EventType,
        related_name="events",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    priority = models.IntegerField(
        _("Priority level"),
        choices=PriorityChoices.choices,
        default=0,
    )
    owner = models.ForeignKey(
        "accounts.Profile",
        related_name="events_owner",
        on_delete=models.CASCADE,
    )
    staff_participants = models.ManyToManyField(
        "accounts.Profile",
        related_name="events",
        verbose_name=_("Staff Participants"),
        blank=True,
    )
    candidate_participants = models.ManyToManyField(
        "candidates.Candidate",
        related_name="events",
        verbose_name=_("Candidate Participants"),
        blank=True,
    )
    start_time = models.DateTimeField(
        _("Event starts at"),
    )
    end_time = models.DateTimeField(
        _("Event ends at"),
    )
    duration = models.DurationField(
        editable=False,
        verbose_name=_("Duration"),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now=True,
    )
    changed_at = models.DateTimeField(
        _("Last updated"),
        auto_now_add=True,
    )
    status = models.IntegerField(
        _("Priority level"),
        choices=EventStatusChoices.choices,
        default=1,
    )

    def __str__(self) -> str:
        """Return title of the Event."""
        return self.title

    def __repr__(self) -> str:
        """Return debug info for the Event."""
        return f"<Event (id={self.id}) - {self.title}>"

    @property
    def is_active(self):
        return self.status == EventStatusChoices.ACTIVE

    @property
    def is_cancelled(self):
        return self.status == EventStatusChoices.CANCELLED

    @property
    def is_completed(self):
        return self.status == EventStatusChoices.COMPLETED

    def mark_as_active(self):
        """Marks event as approved."""
        self.status = EventStatusChoices.ACTIVE
        self.save(update_fields=["status"])

    def mark_as_cancelled(self):
        """Marks event as cancelled."""
        self.status = EventStatusChoices.CANCELLED
        self.save(update_fields=["status"])

    def mark_as_completed(self):
        """Marks event as completed."""
        self.status = EventStatusChoices.COMPLETED
        self.save(update_fields=["status"])
