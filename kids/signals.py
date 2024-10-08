from django.db.models.signals import pre_save
from django.dispatch import receiver
from profiles.models import Profile


@receiver(pre_save, sender=Profile)
def inactivate_kids(sender, instance, **kwargs):
    try:
        current_is_active_profile = Profile.objects.get(pk=instance.pk).is_active
        if instance.is_active != current_is_active_profile:
            profile_kids = instance.user.kids.all()

            for (
                kid
            ) in (
                profile_kids
            ):  # Dont use .update() here you need to call save on each instance
                kid.is_active = instance.is_active
                kid.save()
            return profile_kids
        return None
    except Profile.DoesNotExist:
        return None
