from django.db import models
from django.contrib.auth.models import User





class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete= models.CASCADE)
    image = models.ImageField(blank=True)
    education = models.CharField(max_length=200, blank=True)
    work = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    location = models.CharField(max_length=200),
    followers_count = models.BigIntegerField(default=0)
    following_count = models.BigIntegerField(default=0)
    post_count = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.user)


