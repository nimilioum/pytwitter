from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PostManager(models.Manager):

    def get(self, *args, **kwargs):
        return super(PostManager, self).get(*args, **kwargs).prefetch_related('comments')

    def get_queryset(self):
        return (super(PostManager, self).get_queryset().prefetch_related('user', 'user__profile',
                                                                         'files', 'hashtags', 'mentions')
                .annotate(
            likes_count=models.Count('likes'),
            retweets_count=models.Count('retweets'),
            replies_count=models.Count('comments'),
        )).order_by('-created_at')

    def get_user_likes(self, user: User):
        return self.filter(likes=user)

    def get_user_retweets(self, username: str):
        return self.filter(retweets=username)

    def get_user_tweets(self, username: str):
        return self.filter(user__username=username, reply_to=None)

    def get_user_tweets_replies(self, username: str):
        return self.filter(user=username)

    def get_user_bookmarks(self, user: User):
        return self.filter(saves=user)

