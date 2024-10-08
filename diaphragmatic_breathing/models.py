from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from appointments.models import Appointment


class DiaphragmaticBreathing(BaseModel):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name="diaphragmatic_breathings",
        verbose_name=_("Appointment"),
    )
    date = models.DateTimeField(verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Diaphragmatic Breathing")
        verbose_name_plural = _("Diaphragmatic Breathings")


class TutorialDiaphragmaticBreathing(BaseModel):
    step = models.PositiveIntegerField(verbose_name=_("Step"))
    image = models.ImageField(
        upload_to="tutorialDiaphragmaticBreathing/", verbose_name=_("Image")
    )
    audio = models.FileField(
        upload_to="audioTutorialDiaphragmaticBreathing/",
        verbose_name=_("Audio"),
    )

    class Meta:
        verbose_name = _("Tutorial Diaphragmatic Breathing")
        verbose_name_plural = _("Tutorial Diaphragmatic Breathings")
        ordering = ("step",)
