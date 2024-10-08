from django.db.models.signals import pre_save
from django.dispatch import receiver
from kids.models import Kid


@receiver(pre_save, sender=Kid)
def inactivate_appointments(sender, instance, **kwargs):
    try:
        current_is_active_instance = Kid.objects.get(pk=instance.pk).is_active
        if instance.is_active != current_is_active_instance:
            kid_appointments = instance.appointments.all()

            for (
                appointment
            ) in (
                kid_appointments
            ):  # Dont use .update() here you need to call save on each instance
                appointment.is_active = instance.is_active
                appointment.save()

            return kid_appointments
        return None
    except Kid.DoesNotExist:
        return None
