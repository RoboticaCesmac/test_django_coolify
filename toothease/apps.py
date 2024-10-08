from django.contrib.admin.apps import AdminConfig


class ToothEaseAdminConfig(AdminConfig):
    default_site = "toothease.admin.ToothEaseAdminSite"
