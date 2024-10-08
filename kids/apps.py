from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KidsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kids"
    verbose_name = _("Kids")

    def ready(self):
        import kids.signals
