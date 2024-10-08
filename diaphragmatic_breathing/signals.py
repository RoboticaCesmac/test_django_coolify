from django.db.models.signals import pre_save
from django.dispatch import receiver
from appointments.models import Appointment


@receiver(pre_save, sender=Appointment)
def inactivate_appointments(sender, instance, **kwargs):
    try:
        current_is_active_instance = Appointment.objects.get(pk=instance.pk).is_active
        if instance.is_active != current_is_active_instance:
            appointment_breathings = instance.diaphragmatic_breathings.all()

            for (
                breathing
            ) in (
                appointment_breathings
            ):  # Dont use .update() here you need to call save on each instance
                breathing.is_active = instance.is_active
                breathing.save()

            return appointment_breathings
        return None
    except Appointment.DoesNotExist:
        return None
