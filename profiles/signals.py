from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from profiles.models import Profile

user_model = get_user_model()


@receiver(post_save, sender=user_model)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    try:
        profile = Profile.objects.get(user=instance)
        profile.is_active = instance.is_active
        profile.save()
    except Profile.DoesNotExist:
        pass
