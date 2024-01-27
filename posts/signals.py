from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from utils.helpers import get_hashtags, get_mentions

from .models import Post, Hashtag

User = get_user_model()


@receiver(post_save, sender=Post)
def create_hashtags(sender, instance, created, **kwargs):
    if created:
        tags = get_hashtags(instance.caption)
        tags_exist = Hashtag.objects.filter(name__in=tags)
        tags_not_exist = [Hashtag(name=i) for i in tags if i not in tags_exist.values_list('name', flat=True)]

        Hashtag.objects.bulk_create(tags_not_exist)
        tags = Hashtag.objects.filter(name__in=tags)

        instance.hashtags.add(*tags)


@receiver(post_save, sender=Post)
def create_mentions(sender, instance, created, **kwargs):
    if created:
        mentions = get_mentions(instance.caption)
        users_exist = User.objects.filter(username__in=mentions)

        instance.mentions.add(*users_exist)


@receiver(pre_save, sender=Post)
def parent_post(sender, instance: Post, **kwargs):
    if instance.reply_to is not None:
        parent = instance.reply_to
        if parent.post is not None:
            instance.post = parent.post
        else:
            instance.post = instance.reply_to
