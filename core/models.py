from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InactiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InactiveManager()

    class Meta:
        abstract = True
