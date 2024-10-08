from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.urls import reverse
from .models import (
    DiaphragmaticBreathing,
    TutorialDiaphragmaticBreathing,
)


class DiaphragmaticBreathingAdmin(admin.ModelAdmin):
    list_display = ("id", "appointment_link", "date")
    search_fields = (
        "id",
        "appointment__id",
    )
    readonly_fields = ("appointment_link",)

    def appointment_link(self, obj):
        app_label = obj.appointment._meta.app_label
        model_label = obj.appointment._meta.model_name
        url = reverse(
            f"admin:{app_label}_{model_label}_change", args=(obj.appointment.pk,)
        )
        return mark_safe(f'<a href="{url}">{obj.appointment.pk}</a>')

    appointment_link.short_description = _("Appointment")


admin.site.register(DiaphragmaticBreathing, DiaphragmaticBreathingAdmin)


class TutorialDiaphragmaticBreathingAdmin(admin.ModelAdmin):
    list_display = ("id", "step", "image")
    search_fields = (
        "id",
        "step",
    )


admin.site.register(TutorialDiaphragmaticBreathing, TutorialDiaphragmaticBreathingAdmin)
