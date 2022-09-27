
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from autoslug import AutoSlugField


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

class Tags(models.Model):
    name = models.CharField(max_length = 200, unique=True)
    count = models.BigIntegerField()
    followers = models.ManyToManyField(User)
    slug = AutoSlugField(max_length=200,unique=True,populate_from='name',null=True)

    def get_absolute_url(self):
        return reverse('tagdetails', kwargs={'slug':self.slug})

    def __str__(self):
        return str(self.name)


class Posts(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=400)
    body = RichTextField()
    tags = models.CharField(max_length = 200)
    likes = models.ManyToManyField(User, related_name='likes')
    saved = models.ManyToManyField(User, related_name = 'saved')
    readtime = models.IntegerField()
    coverimage = models.ImageField(blank=True, upload_to = 'cover_images')
    active = models.BooleanField(default = True)
    like_count = models.BigIntegerField(default = 0)
    save_count = models.BigIntegerField(default = 0)
    comment_count = models.BigIntegerField(default = 0)
    slug = AutoSlugField(max_length=200,unique=True,populate_from='title',null=True)

    def get_absolute_url(self):
        return reverse('postdetail', kwargs={'slug':self.slug})

    def __str__(self):
        return str(self.title)
