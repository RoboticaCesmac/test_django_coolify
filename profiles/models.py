from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from core.models import BaseModel
from core.validators import future_date_validator
from core.mixins import AgeMixin


class Profile(AgeMixin, BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    birth_date = models.DateField(
        null=True,
        blank=True,
        validators=[future_date_validator],
        verbose_name=_("Birth Date"),
    )

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
