from django.db.models import Count
from django.db import models


class HashtagManager(models.Manager):

    def get_queryset(self):
        a = super(HashtagManager, self).get_queryset().annotate(
            post_count=Count('posts')
        ).order_by()
        return super(HashtagManager, self).get_queryset().annotate(
            post_count=Count('posts')
        ).order_by()
