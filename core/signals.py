from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in



@receiver(post_save, sender=User)
def blogger_profile(sender, instance, created, **kwargs):
    if created:
       #creates the group bloggers if it doesn't exist
        try:
           group = Group.objects.get(name='bloggers')
        except:
            group, created = Group.objects.get_or_create(name='bloggers')

        #exclude admin from being in group and having profile
        if instance.is_superuser:
            return

        instance.groups.add(group)
        Profile.objects.create(
            user = instance
        )

@receiver(user_logged_in)
def create_profile(sender, user, request, **kwargs):
    profile = Profile.objects.filter(user = user)

    if profile or request.user.is_superuser:
        return
    
    Profile.objects.create(
            user = request.user
        )
