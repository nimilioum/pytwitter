from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PostManager(models.Manager):

    def get_queryset(self):
        return (super(PostManager, self).get_queryset().prefetch_related('user', 'user__profile',
                                                                         'files', 'comments', 'hashtags', 'mentions')
                .annotate(
            likes_count=models.Count('likes'),
            retweets_count=models.Count('retweets'),
        ))

    def get_user_likes(self, user: User):
        return self.filter(likes=user)

    def get_user_retweets(self, user: User):
        return self.filter(followed_by=user.profile)

