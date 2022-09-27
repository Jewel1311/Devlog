from unicodedata import name
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.models import Group
from django.dispatch import receiver


@receiver(post_save, sender=User)
def blogger_profile(sender, instance, created, **kwargs):
    if created:
       #creates the group bloggers if it doesn't exist
        try:
           group = Group.objects.get(name='bloggers')
        except:
            group, created = Group.objects.get_or_create(name='bloggers')

        #exclude admin from being in grop and having profile
        if instance.is_superuser:
            return

        instance.groups.add(group)
        Profile.objects.create(
            user = instance
        )

