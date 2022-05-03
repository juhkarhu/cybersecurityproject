from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, null=True, blank=True)
    email = models.CharField('E-mail', max_length=200, null=True, blank=True)
    phone = models.CharField('Phone number', max_length=50, null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.CharField(max_length=30, null=True, blank=True)


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    postTitle = models.CharField('Post Title', max_length=50)
    postContent = models.CharField('Post Content', max_length=250)
    date = models.DateTimeField(null=False, blank=False,auto_now_add=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()