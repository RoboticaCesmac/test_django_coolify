from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.urls import reverse
from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "kid_link", "doctor", "date", "status", "score")
    search_fields = (
        "id",
        "kid__name",
        "doctor",
        "status",
        "score",
    )
    list_filter = ["status"]

    readonly_fields = ("kid_link",)

    def kid_link(self, obj):
        app_label = obj.kid._meta.app_label
        model_label = obj.kid._meta.model_name
        url = reverse(f"admin:{app_label}_{model_label}_change", args=(obj.kid.pk,))
        return mark_safe(f'<a href="{url}">{obj.kid.name}</a>')

    kid_link.short_description = _("Kid")


admin.site.register(Appointment, AppointmentAdmin)
