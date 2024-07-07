from django.db import models, IntegrityError

from posts.managers import PostManager
from .hashtag import Hashtag
from utils import DomainException
from utils.models import Model
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    caption = models.TextField(max_length=1000)

    retweets = models.ManyToManyField(User, related_name='retweets')
    likes = models.ManyToManyField(User, related_name='liked_posts')
    saves = models.ManyToManyField(User, related_name='saved_posts')

    hashtags = models.ManyToManyField(Hashtag, related_name='posts')
    mentions = models.ManyToManyField(User, related_name='mentions')
    reports = models.ManyToManyField(User, related_name='reports', through='Report')

    post = models.ForeignKey('self', related_name='comments', on_delete=models.CASCADE, null=True)
    reply_to = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True)

    objects = PostManager()

    def is_liked(self, user: User):
        return self.likes.filter(id=user.id).exists()

    def is_retweeted(self, user: User):
        return self.retweets.filter(id=user.id).exists()

    def is_saved(self, user: User):
        return self.saves.filter(id=user.id).exists()

    def retweet(self, user: User):
        if user not in self.retweets.all():
            self._retweet(user)
        else:
            self._unretweet(user)

    def like(self, user: User):
        a = self.likes.all()
        b = user in a
        if user not in self.likes.all():
            self._like(user)
        else:
            self._unlike(user)

    def save_post(self, user: User):
        if user not in self.saves.all():
            self._save(user)
        else:
            self._unsave(user)

    def _retweet(self, user: User):
        try:
            self.retweets.add(user)
        except IntegrityError:
            raise DomainException('Post is already retweeted')

    def _unretweet(self, user: User):
        self.retweets.remove(user)

    def _like(self, user: User):
        try:
            self.likes.add(user)
        except IntegrityError:
            raise DomainException('Post is already liked')

    def _unlike(self, user: User):
        self.likes.remove(user)

    def _save(self, user: User):
        try:
            self.saves.add(user)
        except IntegrityError:
            raise DomainException('Post is already saved')

    def _unsave(self, user: User):
        self.saves.remove(user)

    def is_reply(self):
        return self.reply_to is None


class Upload(Model):
    file = models.FileField(upload_to='files/')
    post = models.ForeignKey(Post, related_name='files', on_delete=models.CASCADE)
