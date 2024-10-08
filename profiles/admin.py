from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "birth_date")
    search_fields = (
        "id",
        "user__username",
    )

    readonly_fields = ("user_link",)

    def user_link(self, obj):
        app_label = obj.user._meta.app_label
        model_label = obj.user._meta.model_name
        url = reverse(f"admin:{app_label}_{model_label}_change", args=(obj.user.pk,))
        return mark_safe(f'<a href="{url}">{obj.user.username}</a>')

    user_link.short_description = _("User")


admin.site.register(Profile, ProfileAdmin)
