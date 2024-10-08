from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DiaphragmaticBreathingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "diaphragmatic_breathing"
    verbose_name = _("Diaphragmatic Breathings")

    def ready(self):
        import diaphragmatic_breathing.signals
