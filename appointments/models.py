from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from core.validators import past_date_validator
from kids.models import Kid

APPOINTMENT_STATUS = (
    ("pending", _("Pending")),
    ("completed", _("Completed")),
    ("cancelled", _("Cancelled")),
)


class Appointment(BaseModel):
    kid = models.ForeignKey(
        Kid,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name=_("Kid"),
    )
    doctor = models.CharField(max_length=255, verbose_name=_("Doctor"))
    date = models.DateTimeField(verbose_name=_("Date"))
    status = models.CharField(
        max_length=20,
        choices=APPOINTMENT_STATUS,
        default="pending",
        verbose_name=_("Status"),
    )
    score = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(10)]
    )

    @property
    def diaphragmatic_breathings_made(self) -> int:
        return self.diaphragmatic_breathings(manager="active_objects").count()

    def __str__(self) -> str:
        return f"{self.id}"

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
