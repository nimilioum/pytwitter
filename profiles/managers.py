from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F

User = get_user_model()


class ProfileManager(models.Manager):

    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().select_related('user').annotate(
            follows_count=models.Count('follows'),
            follower_count=models.Count('followed_by'),
            # tweets=F('tweets'),
            # posts_count=models.Count('tweets', distinct=True),
        )

    def get_user_followings(self, profile):
        return self.filter(followed_by=profile)

    def get_user_followers(self, profile):
        return self.filter(follows=profile)

