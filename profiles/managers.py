from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileManager(models.Manager):

    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().select_related('user').annotate(
            follows_count=models.Count('follows'),
            follower_count=models.Count('followed_by'),
        )

    def get_user_followings(self, user: User):
        return self.filter(follows=user.profile)

    def get_user_followers(self, user: User):
        return self.filter(followed_by=user.profile)

