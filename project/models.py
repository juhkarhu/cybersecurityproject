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


# class Comment(models.Model):
#     poster = models.ForeignKey(User, on_delete=models.CASCADE)
#     relatedPost = models.ForeignKey(Post, on_delete=models.CASCADE)
#     comment = models.TextField('Comment')


# class Message(models.Model):
#     source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='source')
#     target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
#     content = models.TextField()
#     time = models.DateTimeField(auto_now_add=True)


# Extending the base User model of Django's: 
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()