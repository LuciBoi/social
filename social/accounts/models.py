import os
import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from .utils import random_player_id_generator
from django.dispatch import receiver


def get_filename(filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    return name, ext


def add_avatar(instance, filename):
    name, ext = get_filename(filename)
    midName = random.randint(1, 10000000)
    finalName = "{midName}{name}".format(midName=midName, name=name)
    imageName = "{finalName}{ext}".format(finalName=finalName, ext=ext)
    return "{username}/avatar/{imageName}".format(username=instance, imageName=imageName)


class Profiles(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    is_active = models.BooleanField(default=False)
    followed_to = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False)
    avatar = models.ImageField(upload_to=add_avatar, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profiles.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, *args, **kwargs):
    instance.profile.save()
