from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Kid


class KidAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "father_link", "birth_date")
    search_fields = (
        "id",
        "name",
        "father__username",
        "father__first_name",
        "father__last_name",
    )
    readonly_fields = ("father_link",)

    def father_link(self, obj):
        app_label = obj.father._meta.app_label
        model_label = obj.father._meta.model_name
        url = reverse(f"admin:{app_label}_{model_label}_change", args=(obj.father.pk,))
        return mark_safe(f'<a href="{url}">{obj.father.username}</a>')

    father_link.short_description = _("Father")


admin.site.register(Kid, KidAdmin)
