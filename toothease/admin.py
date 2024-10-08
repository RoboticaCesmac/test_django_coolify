from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class ToothEaseAdminSite(admin.AdminSite):
    site_header = _("Toothease Administration")
    site_title = _("Toothease Admin")
    index_title = _("Toothease Admin")
