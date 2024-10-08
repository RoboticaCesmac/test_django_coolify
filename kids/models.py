from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from core.mixins import AgeMixin
from core.models import BaseModel
from core.validators import future_date_validator

user_model = get_user_model()


class Kid(AgeMixin, BaseModel):
    father = models.ForeignKey(
        user_model,
        related_name="kids",
        on_delete=models.CASCADE,
        verbose_name=_("Father"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    birth_date = models.DateField(
        validators=[future_date_validator], verbose_name=_("Birth Date")
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _("Kid")
        verbose_name_plural = _("Kids")
