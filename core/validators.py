import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def future_date_validator(value):
    if value > datetime.date.today():
        raise ValidationError(_("Birth date cannot be in the future."))


def past_date_validator(value):
    if value < timezone.now():
        raise ValidationError(_("Appointment date cannot be in the past."))
