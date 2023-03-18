from email.policy import default
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from autoslug import AutoSlugField
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete= models.CASCADE)
    image = models.ImageField(upload_to="profile_image/",blank=True)
    education = models.CharField(max_length=200, blank=True)
    work = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    location = models.CharField(max_length=200, default="", null=True)
    connections = models.ManyToManyField(User,related_name='followers')
    followers_count = models.BigIntegerField(default=0)
    following_count = models.BigIntegerField(default=0)
    post_count = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.user)

class Tags(models.Model):
    name = models.CharField(max_length = 200, unique=True)
    count = models.BigIntegerField()
    followers = models.ManyToManyField(User, related_name= 'tagfollower')
    slug = AutoSlugField(max_length=200,unique=True,populate_from='name',null=True)
    follower_count = models.BigIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug':self.slug})

    @classmethod
    def get_tag(self,tag):
        try:
            return self.objects.get(name = tag)         
        except:
            return None


    def __str__(self):
        return str(self.name)


class Posts(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=400)
    body = RichTextField()
    tags = models.ManyToManyField(Tags)
    likes = models.ManyToManyField(User, related_name='liked')
    saved = models.ManyToManyField(User, related_name = 'saves')
    readtime = models.IntegerField()
    coverimage = models.ImageField(blank=True, upload_to = 'cover_images/')
    active = models.BooleanField(default = True)
    like_count = models.BigIntegerField(default = 0)
    save_count = models.BigIntegerField(default = 0)
    comment_count = models.BigIntegerField(default = 0)
    slug = AutoSlugField(max_length=200,unique=True,populate_from='title',null=True)
    draft = models.BooleanField(default=False)
    report_count = models.BigIntegerField(default=0)


    def get_absolute_url(self):
        return reverse('read_post', kwargs={'slug':self.slug})

    def save(self):
        super().save()  # saving image first
        if self.coverimage:
            img = Image.open(self.coverimage.path) # Open image using self
            if img.height > 300 or img.width > 300:
                new_img = (300, 300)
                img.thumbnail(new_img)
                img.save(self.coverimage.path)  # saving image at the same path

    @classmethod
    def get_recent_posts(self):
        return self.objects.filter(active=True, draft = False).order_by('-id')

    @classmethod
    def get_top_posts(self):
        return self.objects.filter(active=True, draft = False).order_by('-like_count')

    @classmethod    
    def get_tag_post(self, tag):
        return self.objects.filter(tags = tag, active=True, draft = False).order_by('-id')

        
    def __str__(self):
        return str(self.title)

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    body = models.TextField(default="")
    reply_count = models.IntegerField(default=0)

class Replies(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="rcomment")
    mention = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="to_mention")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    body = models.TextField(default="")

class PostReports(models.Model):
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)
    category = models.CharField(max_length = 100)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateTimeField()


